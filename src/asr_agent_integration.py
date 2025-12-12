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

from src.inference import vad_split, transcribe_audio, normalize_text

# Import agent core
from src.orchestrator import AlgerianAgentOrchestrator

# ⚡ Bolt Optimization: Global cache for ASR models.
# This prevents reloading the model from disk on every pipeline instantiation,
# which is a very slow operation.
_asr_model_cache = {}

def _load_asr_model(model_name: str) -> Tuple[WhisperProcessor, WhisperForConditionalGeneration]:
    """Loads ASR model from cache or from Hugging Face if not cached."""
    if model_name in _asr_model_cache:
        print(f"Loading ASR model from cache: {model_name}")
        return _asr_model_cache[model_name]

    print(f"Loading and caching ASR model: {model_name}")
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
        asr_model_name: str = "openai/whisper-small",
        tenant_config: Optional[Dict] = None
    ):
        """
        Initialize voice agent pipeline

        Args:
            asr_model_name: Hugging Face model name for ASR
            tenant_config: Business configuration for agent
        """
        # Load ASR components using the caching mechanism
        self.asr_processor, self.asr_model = _load_asr_model(asr_model_name)

        # Initialize agent
        self.tenant_config = tenant_config or self._default_tenant_config()
        self.agent = AlgerianAgentOrchestrator(self.tenant_config)

        print("Voice Agent Pipeline initialized")

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

        Args:
            audio_path: Path to audio file
            customer_id: Customer identifier
            conversation_id: Optional existing conversation ID

        Returns:
            Full interaction result with transcription and agent response
        """

        print(f"\n{'='*80}")
        print(f"Processing voice call from: {customer_id}")
        print(f"Audio file: {audio_path}")
        print(f"{'='*80}\n")

        # Step 1: Transcribe audio
        print("Step 1: Transcribing audio...")
        transcription = await self._transcribe_audio(audio_path)
        print(f"Transcription: {transcription}")

        # Step 2: Process through agent
        print("\nStep 2: Processing through agent...")
        agent_response = await self._process_with_agent(
            transcription,
            customer_id,
            conversation_id
        )

        # Step 3: Generate TTS response (placeholder)
        print("\nStep 3: Generating voice response...")
        audio_response_path = await self._generate_tts_response(
            agent_response['response']
        )

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
                'toxic_detected': agent_response.get('metadata', {}).get('toxic_detected', False)
            }
        }

        print(f"\n{'='*80}")
        print(f"Call processing complete")
        print(f"Intent: {result['metadata']['intent']}")
        print(f"Agent Response: {agent_response['response']}")
        print(f"{'='*80}\n")

        return result

    async def _transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio using Whisper ASR"""

        # Perform VAD and split
        audio, speech_chunks = vad_split(audio_path)

        if not speech_chunks:
            return "[No speech detected]"

        # Transcribe audio chunks
        transcription = transcribe_audio(
            self.asr_model,
            self.asr_processor,
            audio,
            speech_chunks
        )

        # Normalize
        normalized = normalize_text(transcription)

        return normalized if normalized.strip() else "[Empty transcription]"

    async def _process_with_agent(
        self,
        transcription: str,
        customer_id: str,
        conversation_id: Optional[str] = None
    ) -> Dict:
        """Process transcription through agent"""

        # In production, use real agent
        return await self.agent.process_message(
            message=transcription,
            customer_id=customer_id,
            tenant_id=self.tenant_config['tenant_id'],
            conversation_id=conversation_id
        )


    async def _generate_tts_response(self, response_text: str) -> str:
        """Generate TTS audio response (placeholder)"""

        # In production, integrate with TTS system
        # For now, return placeholder path
        output_path = f"output/response_{datetime.now().timestamp()}.wav"

        # Would generate actual audio here
        print(f"[TTS] Would generate audio: '{response_text}' -> {output_path}")

        return output_path

    def save_interaction_log(self, result: Dict, output_dir: str = "logs"):
        """Save interaction log for analysis"""

        Path(output_dir).mkdir(exist_ok=True)

        log_file = Path(output_dir) / f"interaction_{result['conversation_id']}.json"

        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"Interaction log saved: {log_file}")


class BatchVoiceProcessor:
    """Process multiple voice calls from dataset"""

    def __init__(self, pipeline: VoiceAgentPipeline):
        self.pipeline = pipeline

    async def process_dataset(
        self,
        dataset_path: str,
        output_dir: str = "results",
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Process dataset of voice calls

        Args:
            dataset_path: Path to dataset directory with audio files
            output_dir: Output directory for results
            limit: Optional limit on number of files to process

        Returns:
            List of processing results
        """

        dataset_dir = Path(dataset_path)
        audio_files = list(dataset_dir.glob("*.wav")) + list(dataset_dir.glob("*.mp3"))

        if limit:
            audio_files = audio_files[:limit]

        print(f"\nProcessing {len(audio_files)} audio files from {dataset_path}")

        results = []
        for i, audio_file in enumerate(audio_files, 1):
            print(f"\n[{i}/{len(audio_files)}] Processing: {audio_file.name}")

            try:
                result = await self.pipeline.process_voice_call(
                    audio_path=str(audio_file),
                    customer_id=f"customer_{audio_file.stem}"
                )
                results.append(result)

                # Save individual result
                self.pipeline.save_interaction_log(result, output_dir)

            except Exception as e:
                print(f"Error processing {audio_file.name}: {e}")
                results.append({
                    'audio_file': str(audio_file),
                    'error': str(e),
                    'status': 'failed'
                })

        # Save summary
        self._save_summary(results, output_dir)

        return results

    def _save_summary(self, results: List[Dict], output_dir: str):
        """Save processing summary"""

        summary = {
            'total_processed': len(results),
            'successful': sum(1 for r in results if 'error' not in r),
            'failed': sum(1 for r in results if 'error' in r),
            'intents': {},
            'languages': {},
            'toxic_detected': sum(
                1 for r in results
                if 'metadata' in r and r['metadata'].get('toxic_detected')
            )
        }

        # Count intents and languages
        for result in results:
            if 'metadata' in result:
                intent = result['metadata'].get('intent', 'unknown')
                summary['intents'][intent] = summary['intents'].get(intent, 0) + 1

                lang = result.get('transcription', {}).get('language', 'unknown')
                summary['languages'][lang] = summary['languages'].get(lang, 0) + 1

        summary_file = Path(output_dir) / 'processing_summary.json'
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        print(f"\n{'='*80}")
        print("Processing Summary:")
        print(f"  Total: {summary['total_processed']}")
        print(f"  Successful: {summary['successful']}")
        print(f"  Failed: {summary['failed']}")
        print(f"  Toxic detected: {summary['toxic_detected']}")
        print(f"\nIntent distribution:")
        for intent, count in summary['intents'].items():
            print(f"  {intent}: {count}")
        print(f"\nSummary saved: {summary_file}")
        print(f"{'='*80}\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    """Main execution for testing"""

    # Initialize pipeline
    tenant_config = {
        'tenant_id': 'algerian_telecom',
        'business_name': 'Algérie Télécom',
        'business_type': 'telecommunications',
        'language_preference': 'darija'
    }

    pipeline = VoiceAgentPipeline(
        asr_model_name="openai/whisper-small",
        tenant_config=tenant_config
    )

    # Example 1: Process single call
    print("\n" + "="*80)
    print("EXAMPLE 1: Single Voice Call Processing")
    print("="*80)

    # This would use actual audio file from your repo
    # result = await pipeline.process_voice_call(
    #     audio_path="sample_audio.wav",
    #     customer_id="cust_001"
    # )

    # Example 2: Batch processing
    print("\n" + "="*80)
    print("EXAMPLE 2: Batch Dataset Processing")
    print("="*80)

    batch_processor = BatchVoiceProcessor(pipeline)

    # This would process your audio dataset
    # results = await batch_processor.process_dataset(
    #     dataset_path="data/audio_samples",
    #     output_dir="results/batch_processing",
    #     limit=10
    # )

    print("\n✓ Pipeline demonstration complete")
    print("To use with real audio files:")
    print("  1. Place audio files in data/audio_samples/")
    print("  2. Uncomment the processing calls above")
    print("  3. Run: python asr_agent_integration.py")


if __name__ == "__main__":
    asyncio.run(main())
