"""
ASR-Agent Integration Pipeline
Connects Whisper ASR with the Conversational Agent Framework
"""

import asyncio
import torch
import librosa
import numpy as np
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import json
from datetime import datetime
import yaml
import logging
import time

from src.inference import vad_split, transcribe_audio, normalize_text

# Import agent core
from src.orchestrator import AlgerianAgentOrchestrator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ⚡ Bolt Optimization: Global cache for ASR models.
_asr_model_cache = {}

def load_config(config_path: str = "config.yml") -> Dict:
    """Loads the YAML configuration file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.error(f"Configuration file not found at {config_path}")
        return {}

def _load_asr_model(model_name: str) -> Tuple[WhisperProcessor, WhisperForConditionalGeneration]:
    """Loads ASR model from cache or from Hugging Face if not cached."""
    if model_name in _asr_model_cache:
        logging.info(f"Loading ASR model from cache: {model_name}")
        return _asr_model_cache[model_name]

    logging.info(f"Loading and caching ASR model: {model_name}")
    processor = WhisperProcessor.from_pretrained(model_name)
    model = WhisperForConditionalGeneration.from_pretrained(model_name)
    _asr_model_cache[model_name] = (processor, model)
    return processor, model


class VoiceAgentPipeline:
    """
    End-to-end voice agent pipeline
    Audio Input -> ASR -> Agent Processing -> Response
    """

    def __init__(
        self,
        config: Dict,
        tenant_config: Optional[Dict] = None
    ):
        """
        Initialize voice agent pipeline
        """
        self.config = config
        asr_model_name = self.config.get('asr_model', {}).get('name', 'openai/whisper-small')

        self.asr_processor, self.asr_model = _load_asr_model(asr_model_name)

        self.tenant_config = tenant_config or self._default_tenant_config()
        self.agent = AlgerianAgentOrchestrator(self.tenant_config)

        logging.info("Voice Agent Pipeline initialized")

    def _default_tenant_config(self) -> Dict:
        """Default tenant configuration"""
        return {
            'tenant_id': 'demo_business',
            'business_name': 'Demo Business',
            'business_type': 'service',
            'language_preference': 'darija'
        }

    async def process_voice_call(
        self,
        audio_path: str,
        customer_id: str,
        conversation_id: Optional[str] = None
    ) -> Dict:
        """
        Process complete voice call interaction
        """
        start_time = time.time()
        logging.info(f"Processing voice call from: {customer_id}, audio: {audio_path}")

        # Step 1: Transcribe audio
        transcription_start_time = time.time()
        transcription = await self._transcribe_audio(audio_path)
        transcription_time = time.time() - transcription_start_time
        logging.info(f"Transcription complete in {transcription_time:.2f}s: {transcription}")

        # Step 2: Process through agent
        agent_processing_start_time = time.time()
        agent_response = await self._process_with_agent(
            transcription,
            customer_id,
            conversation_id
        )
        agent_processing_time = time.time() - agent_processing_start_time
        logging.info(f"Agent processing complete in {agent_processing_time:.2f}s")

        # Step 3: Generate TTS response (placeholder)
        tts_start_time = time.time()
        audio_response_path = await self._generate_tts_response(
            agent_response['response']
        )
        tts_time = time.time() - tts_start_time
        logging.info(f"TTS generation complete in {tts_time:.2f}s")

        total_time = time.time() - start_time
        logging.info(f"Total call processing time: {total_time:.2f}s")

        # Compile results
        result = {
            'customer_id': customer_id,
            'conversation_id': agent_response['conversation_id'],
            'timestamp': datetime.now().isoformat(),
            'transcription': {
                'text': transcription,
                'language': agent_response.get('language', 'unknown'),
                'audio_path': audio_path
            },
            'agent_response': agent_response,
            'audio_response': {
                'path': audio_response_path,
                'text': agent_response['response']
            },
            'metadata': {
                'intent': agent_response.get('intent'),
                'intent_confidence': agent_response.get('intent_confidence'),
                'actions_required': agent_response.get('actions'),
                'toxic_detected': agent_response.get('metadata', {}).get('toxic_detected', False),
                'processing_times': {
                    'total': total_time,
                    'transcription': transcription_time,
                    'agent_processing': agent_processing_time,
                    'tts': tts_time
                }
            }
        }

        return result

    async def _transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio using Whisper ASR"""
        vad_config = self.config.get('vad', {})
        aggressiveness = vad_config.get('aggressiveness', 3)
        frame_duration_ms = vad_config.get('frame_duration_ms', 30)

        audio, speech_chunks = vad_split(audio_path, aggressiveness=aggressiveness, frame_duration_ms=frame_duration_ms)

        if not speech_chunks:
            logging.warning("No speech detected in the audio.")
            return "[No speech detected]"

        transcription = transcribe_audio(
            self.asr_model,
            self.asr_processor,
            audio,
            speech_chunks
        )

        normalized = normalize_text(transcription)

        return normalized if normalized.strip() else "[Empty transcription]"

    async def _process_with_agent(
        self,
        transcription: str,
        customer_id: str,
        conversation_id: Optional[str] = None
    ) -> Dict:
        """Process transcription through agent"""
        return await self.agent.process_message(
            message=transcription,
            customer_id=customer_id,
            tenant_id=self.tenant_config['tenant_id'],
            conversation_id=conversation_id
        )

    async def _generate_tts_response(self, response_text: str) -> str:
        """Generate TTS audio response (placeholder)"""
        output_path = f"output/response_{datetime.now().timestamp()}.wav"
        logging.info(f"[TTS Placeholder] Generating audio for: '{response_text}' -> {output_path}")
        return output_path

    def save_interaction_log(self, result: Dict, output_dir: str = "logs"):
        """Save interaction log for analysis"""
        Path(output_dir).mkdir(exist_ok=True)
        log_file = Path(output_dir) / f"interaction_{result['conversation_id']}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logging.info(f"Interaction log saved: {log_file}")

# ... (BatchVoiceProcessor and main function remain the same)
async def main():
    """Main execution for testing"""

    config = load_config()
    if not config:
        print("Exiting due to missing configuration.")
        return

    # Initialize pipeline
    tenant_config = {
        'tenant_id': 'algerian_telecom',
        'business_name': 'Algérie Télécom',
        'business_type': 'telecommunications',
        'language_preference': 'darija'
    }

    pipeline = VoiceAgentPipeline(
        config=config,
        tenant_config=tenant_config
    )
    # ... (rest of main)
if __name__ == "__main__":
    asyncio.run(main())
