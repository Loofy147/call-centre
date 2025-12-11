"""
Production API Server for Algerian Voice Agent System
FastAPI-based REST API with WhatsApp integration
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import asyncio
import aioredis
import uuid
from datetime import datetime
import io
import json
import os

from src.orchestrator import AlgerianAgentOrchestrator
from src.asr_agent_integration import VoiceAgentPipeline


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class TextMessageRequest(BaseModel):
    """Request model for text-based interaction"""
    message: str = Field(..., description="Customer message text")
    customer_id: str = Field(..., description="Customer identifier")
    tenant_id: str = Field(..., description="Business/tenant identifier")
    conversation_id: Optional[str] = Field(None, description="Existing conversation ID")
    language: Optional[str] = Field(None, description="Preferred language")


class VoiceMessageRequest(BaseModel):
    """Request model for voice-based interaction"""
    customer_id: str
    tenant_id: str
    conversation_id: Optional[str] = None
    audio_format: str = "wav"


class AgentResponse(BaseModel):
    """Response model for agent interactions"""
    conversation_id: str
    response: str
    intent: str
    intent_confidence: float
    language: str
    entities: Dict[str, List[Dict]]
    actions: Optional[str]
    requires_input: bool
    timestamp: str
    metadata: Dict[str, Any]


class ConversationHistory(BaseModel):
    """Conversation history response"""
    conversation_id: str
    customer_id: str
    tenant_id: str
    messages: List[Dict]
    created_at: str
    updated_at: str


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    services: Dict[str, str]


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="Algerian Voice Agent API",
    description="AI-powered conversational agents for Algerian businesses",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# GLOBAL STATE (In production, use proper dependency injection)
# ============================================================================

class ApplicationState:
    """Global application state"""

    def __init__(self):
        self.redis_client = None
        self.voice_pipelines: Dict[str, Any] = {}
        self.agent_orchestrators: Dict[str, Any] = {}

    async def initialize(self):
        """Initialize application state"""
        # Connect to Redis
        redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
        try:
            self.redis_client = await aioredis.create_redis_pool(
                redis_url,
                encoding='utf-8'
            )
            print("✓ Connected to Redis")
        except Exception as e:
            print(f"⚠ Redis connection failed: {e}")
            self.redis_client = None

        # Initialize default tenant
        await self.load_tenant('demo_tenant')

    async def load_tenant(self, tenant_id: str):
        """Load tenant configuration and initialize services"""

        # In production, load from database
        tenant_config = {
            'tenant_id': tenant_id,
            'business_name': 'Demo Business',
            'business_type': 'service',
            'language_preference': 'darija'
        }

        # Initialize voice pipeline for tenant
        self.voice_pipelines[tenant_id] = VoiceAgentPipeline(
            tenant_config=tenant_config
        )

        # Initialize agent orchestrator
        self.agent_orchestrators[tenant_id] = AlgerianAgentOrchestrator(
            tenant_config=tenant_config,
            redis_client=self.redis_client
        )

        print(f"✓ Loaded tenant: {tenant_id}")

    async def cleanup(self):
        """Cleanup resources"""
        if self.redis_client:
            self.redis_client.close()
            await self.redis_client.wait_closed()


# Global state instance
state = ApplicationState()


# ============================================================================
# STARTUP & SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Application startup"""
    print("\n" + "="*80)
    print("Starting Algerian Voice Agent API")
    print("="*80)
    await state.initialize()
    print("✓ Application ready")
    print("="*80 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    print("\nShutting down...")
    await state.cleanup()
    print("✓ Cleanup complete")


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "service": "Algerian Voice Agent API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        services={
            "api": "up",
            "redis": "up" if state.redis_client else "down",
            "asr": "up",
            "agent": "up"
        }
    )


@app.post("/api/v1/message/text", response_model=AgentResponse)
async def process_text_message(request: TextMessageRequest):
    """
    Process text message from customer

    Endpoint for WhatsApp, web chat, SMS integrations
    """

    try:
        # Get agent orchestrator for tenant
        agent = state.agent_orchestrators.get(request.tenant_id)
        if not agent:
            await state.load_tenant(request.tenant_id)
            agent = state.agent_orchestrators[request.tenant_id]

        # Process message
        response_data = await agent.process_message(
            message=request.message,
            customer_id=request.customer_id,
            tenant_id=request.tenant_id,
            conversation_id=request.conversation_id
        )

        # Adapt response to fit the AgentResponse model
        response_data['timestamp'] = response_data['metadata']['timestamp']

        return AgentResponse(**response_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/message/voice")
async def process_voice_message(
    audio: UploadFile = File(...),
    customer_id: str = "default",
    tenant_id: str = "demo_tenant",
    conversation_id: Optional[str] = None
):
    """
    Process voice message from customer

    Endpoint for phone calls, voice messages
    """

    try:
        # Save uploaded audio temporarily
        audio_bytes = await audio.read()
        temp_audio_path = f"/tmp/audio_{uuid.uuid4()}.wav"

        with open(temp_audio_path, 'wb') as f:
            f.write(audio_bytes)

        # Get voice pipeline for tenant
        pipeline = state.voice_pipelines.get(tenant_id)
        if not pipeline:
            await state.load_tenant(tenant_id)
            pipeline = state.voice_pipelines[tenant_id]

        # Process voice call
        result = await pipeline.process_voice_call(
            audio_path=temp_audio_path,
            customer_id=customer_id,
            conversation_id=conversation_id
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/reservation/create")
async def create_reservation(
    conversation_id: str,
    reservation_details: Dict[str, Any]
):
    """Create reservation from confirmed details"""

    try:
        # In production, save to database
        reservation = {
            "reservation_id": str(uuid.uuid4()),
            "conversation_id": conversation_id,
            "status": "confirmed",
            "created_at": datetime.now().isoformat(),
            **reservation_details
        }

        # Send confirmation via WhatsApp/SMS
        # await send_confirmation(reservation)

        return reservation

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/conversation/{tenant_id}/{conversation_id}", response_model=ConversationHistory)
async def get_conversation_history(tenant_id: str, conversation_id: str):
    """Retrieve conversation history"""

    try:
        agent = state.agent_orchestrators.get(tenant_id)
        if not agent:
             raise HTTPException(status_code=404, detail=f"Agent for tenant '{tenant_id}' not found")

        history = await agent.get_conversation_history(conversation_id)
        if not history:
            raise HTTPException(status_code=404, detail="Conversation not found")

        context = await agent._get_or_create_context(conversation_id, tenant_id, "")

        history_data = {
            "conversation_id": conversation_id,
            "customer_id": context.customer_id,
            "tenant_id": context.tenant_id,
            "messages": history,
            "created_at": context.created_at.isoformat(),
            "updated_at": context.updated_at.isoformat()
        }

        return ConversationHistory(**history_data)

    except Exception as e:
        raise HTTPException(status_code=404, detail="Conversation not found")


@app.delete("/api/v1/conversation/{tenant_id}/{conversation_id}")
async def end_conversation(tenant_id: str, conversation_id: str):
    """End conversation and cleanup"""

    try:
        agent = state.agent_orchestrators.get(tenant_id)
        if agent:
            await agent.end_conversation(conversation_id)

        return {"status": "conversation_ended", "conversation_id": conversation_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/analytics/summary")
async def get_analytics_summary(
    tenant_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Get analytics summary for tenant"""

    # In production, query from analytics database
    return {
        "tenant_id": tenant_id,
        "period": {"start": start_date, "end": end_date},
        "metrics": {
            "total_conversations": 1523,
            "avg_response_time": 2.3,
            "customer_satisfaction": 4.2,
            "intent_distribution": {
                "reservation": 45,
                "inquiry": 30,
                "complaint": 15,
                "technical_support": 10
            },
            "language_distribution": {
                "darija": 60,
                "french": 30,
                "mixed": 10
            },
            "toxic_detected": 3
        }
    }


# ============================================================================
# WHATSAPP WEBHOOK
# ============================================================================

@app.post("/webhooks/whatsapp")
async def whatsapp_webhook(payload: Dict[str, Any], background_tasks: BackgroundTasks):
    """
    WhatsApp Business API webhook
    Processes incoming messages from WhatsApp
    """

    try:
        # Parse WhatsApp payload
        message_data = payload.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {})
        messages = message_data.get('messages', [])

        if not messages:
            return {"status": "no_messages"}

        message = messages[0]
        customer_phone = message.get('from')
        message_type = message.get('type')

        # Extract message content
        if message_type == 'text':
            text_content = message.get('text', {}).get('body', '')

            # Process in background
            background_tasks.add_task(
                process_whatsapp_text,
                customer_phone,
                text_content
            )

        elif message_type == 'audio':
            audio_id = message.get('audio', {}).get('id')

            # Process in background
            background_tasks.add_task(
                process_whatsapp_audio,
                customer_phone,
                audio_id
            )

        return {"status": "processing"}

    except Exception as e:
        print(f"WhatsApp webhook error: {e}")
        return {"status": "error", "message": str(e)}


async def process_whatsapp_text(customer_phone: str, text: str):
    """Process text message from WhatsApp"""

    # Process through agent
    response = await process_text_message(TextMessageRequest(
        message=text,
        customer_id=customer_phone,
        tenant_id='whatsapp_tenant'
    ))

    # Send response back via WhatsApp API
    # await send_whatsapp_message(customer_phone, response.response)


async def process_whatsapp_audio(customer_phone: str, audio_id: str):
    """Process audio message from WhatsApp"""

    # Download audio from WhatsApp
    # audio_bytes = await download_whatsapp_audio(audio_id)

    # Process through voice pipeline
    # ... implementation


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================



# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("\n" + "="*80)
    print("Starting Algerian Voice Agent API Server")
    print("="*80 + "\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
