
import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import asdict
import redis
from src.models import ConversationContext, LanguageContext, Language
from src.classifiers import AlgerianLanguageDetector
from src.ml_classifier import MLIntentClassifier
from src.entity_extractor import EntityExtractor
from src.response_generator import ResponseGenerator

class AlgerianAgentOrchestrator:
    """Main orchestrator for the conversational agent system"""

    def __init__(self, tenant_config: Dict, redis_client=None):
        self.tenant_config = tenant_config
        self.language_detector = AlgerianLanguageDetector()
        self.intent_classifier = MLIntentClassifier()
        self.entity_extractor = EntityExtractor()
        self.response_generator = ResponseGenerator(tenant_config)
        self.redis_client = redis_client

    async def process_message(self, message: str, customer_id: str, tenant_id: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        context = await self._get_or_create_context(conversation_id, tenant_id, customer_id)
        conversation_id = context.conversation_id

        lang_ctx = self.language_detector.detect(message)
        context.language_context = lang_ctx

        intent = self.intent_classifier.classify(message)
        context.intent_history.append(intent)

        entities = self.entity_extractor.extract(message, intent)
        context.entities.update(entities)

        response = self.response_generator.generate(intent, entities, context)

        context.conversation_history.append({'role': 'customer', 'message': message})
        context.conversation_history.append({'role': 'agent', 'message': response['text']})

        await self._save_context(context)

        return {
            'conversation_id': conversation_id,
            'response': response['text'],
            'intent': intent.type.value,
            'language': lang_ctx.primary.value,
            **response
        }

    async def _get_or_create_context(self, conversation_id: Optional[str], tenant_id: str, customer_id: str) -> ConversationContext:
        if conversation_id and self.redis_client:
            context_json = await self.redis_client.get(f"session:{conversation_id}")
            if context_json:
                data = json.loads(context_json)
                data['created_at'] = datetime.fromisoformat(data['created_at'])
                data['updated_at'] = datetime.fromisoformat(data['updated_at'])
                return ConversationContext(**data)

        return ConversationContext(
            conversation_id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            customer_id=customer_id,
            language_context=LanguageContext(primary=Language.DARIJA)
        )

    async def _save_context(self, context: ConversationContext):
        context.updated_at = datetime.now()
        if self.redis_client:
            await self.redis_client.set(f"session:{context.conversation_id}", json.dumps(asdict(context), default=str), ex=3600)
