
import argparse
import torch
import librosa
import numpy as np
import webrtcvad
from transformers import WhisperForConditionalGeneration, WhisperProcessor

def vad_split(audio_path, sample_rate=16000, frame_duration_ms=30, vad_aggressiveness=3):
    """
    Splits audio into chunks using Voice Activity Detection (VAD).
    """
    vad = webrtcvad.Vad(vad_aggressiveness)
    audio, sr = librosa.load(audio_path, sr=sample_rate, mono=True)

    if sr != sample_rate:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=sample_rate)

    # Convert audio to 16-bit PCM
    audio_int16 = (audio * 32767).astype(np.int16)

    frame_size = int(sample_rate * (frame_duration_ms / 1000.0))
    chunks = []
    offset = 0

    while offset + frame_size < len(audio_int16):
        frame = audio_int16[offset:offset + frame_size]
        is_speech = vad.is_speech(frame.tobytes(), sample_rate)
        chunks.append({'offset': offset, 'is_speech': is_speech})
        offset += frame_size

    speech_chunks = []
    is_speaking = False
    start_time = 0

    for i, chunk in enumerate(chunks):
        if chunk['is_speech'] and not is_speaking:
            is_speaking = True
            start_time = chunk['offset'] / sample_rate
        elif not chunk['is_speech'] and is_speaking:
            is_speaking = False
            end_time = chunk['offset'] / sample_rate
            speech_chunks.append({'start': start_time, 'end': end_time})

    if is_speaking:
        speech_chunks.append({'start': start_time, 'end': len(audio) / sample_rate})

    return audio, speech_chunks

def transcribe_audio(model, processor, audio, speech_chunks, sample_rate=16000):
    """
    Transcribes audio chunks using the provided model and processor.
    """
    transcriptions = []
    for chunk in speech_chunks:
        start_sample = int(chunk['start'] * sample_rate)
        end_sample = int(chunk['end'] * sample_rate)
        audio_chunk = audio[start_sample:end_sample]

        input_features = processor(audio_chunk, sampling_rate=sample_rate, return_tensors="pt").input_features
        predicted_ids = model.generate(input_features)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        transcriptions.append(transcription)

    return " ".join(transcriptions)

def normalize_text(text):
    """
    Performs basic text normalization.
    """
    text = text.lower()
    # Add more normalization rules here if needed
    return text

def main():
    parser = argparse.ArgumentParser(description="ASR inference script.")
    parser.add_argument("--model-name", type=str, default="openai/whisper-tiny", help="Name of the Hugging Face model to use.")
    parser.add_argument("--audio-file", type=str, required=True, help="Path to the audio file to transcribe.")
    args = parser.parse_args()

    # Load model and processor
    processor = WhisperProcessor.from_pretrained(args.model_name)
    model = WhisperForConditionalGeneration.from_pretrained(args.model_name)

    # Perform VAD and transcribe
    audio, speech_chunks = vad_split(args.audio_file)
    transcription = transcribe_audio(model, processor, audio, speech_chunks)

    # Normalize and print transcription
    normalized_transcription = normalize_text(transcription)
    print(normalized_transcription)

if __name__ == "__main__":
    main()
