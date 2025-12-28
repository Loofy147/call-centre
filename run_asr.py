import argparse
from src.asr import ASR

def main():
    parser = argparse.ArgumentParser(description='ASR inference script.')
    parser.add_argument('--audio-file', type=str, required=True, help='Path to the audio file.')
    parser.add_argument('--model-name', type=str, default='openai/whisper-tiny', help='Name of the ASR model to use.')
    parser.add_argument('--device', type=str, default='cpu', help='Device to run the model on (e.g., "cpu", "cuda").')
    args = parser.parse_args()

    asr = ASR(model_name=args.model_name, device=args.device)
    audio, speech_chunks = asr.vad_split(args.audio_file)
    transcription = asr.transcribe_audio(audio, speech_chunks)
    normalized_transcription = asr.normalize_text(transcription)

    print(f'Transcription: {transcription}')
    print(f'Normalized Transcription: {normalized_transcription}')

if __name__ == '__main__':
    main()
