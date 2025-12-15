
import webrtcvad
import librosa
import numpy as np
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from typing import List, Dict, Tuple
import re

# Helper function to read audio files
def read_wave(path: str) -> Tuple[bytes, int]:
    """Reads a .wav file and returns the audio data and sample rate."""
    audio, sample_rate = librosa.load(path, sr=16000, mono=True)
    # Convert to 16-bit PCM bytes
    pcm_data = (audio * 32767).astype(np.int16).tobytes()
    return pcm_data, sample_rate

def vad_split(audio_path: str, aggressiveness: int = 3, frame_duration_ms: int = 30) -> Tuple[np.ndarray, List[Dict[str, int]]]:
    """
    Performs Voice Activity Detection (VAD) on an audio file and splits it into speech chunks.
    """
    audio, sample_rate = librosa.load(audio_path, sr=16000, mono=True)
    pcm_data = (audio * 32767).astype(np.int16).tobytes()

    vad = webrtcvad.Vad(aggressiveness)

    frame_samples = int(sample_rate * frame_duration_ms / 1000)

    speech_chunks = []
    is_speech = False
    start_frame = 0

    for i in range(0, len(pcm_data), frame_samples * 2): # *2 because it's 16-bit
        frame = pcm_data[i:i + frame_samples * 2]
        if len(frame) < frame_samples * 2:
            break

        current_frame_is_speech = vad.is_speech(frame, sample_rate)

        if not is_speech and current_frame_is_speech:
            start_frame = i // (frame_samples * 2)
            is_speech = True
        elif is_speech and not current_frame_is_speech:
            end_frame = i // (frame_samples * 2)
            speech_chunks.append({
                "start": start_frame * frame_duration_ms,
                "end": end_frame * frame_duration_ms
            })
            is_speech = False

    if is_speech: # If the audio ends on a speech segment
        end_frame = len(pcm_data) // (frame_samples * 2)
        speech_chunks.append({
            "start": start_frame * frame_duration_ms,
            "end": end_frame * frame_duration_ms
        })

    return audio, speech_chunks

def transcribe_audio(model: WhisperForConditionalGeneration, processor: WhisperProcessor, audio: np.ndarray, speech_chunks: List[Dict[str, int]]) -> str:
    """
    Transcribes audio chunks using the Whisper ASR model.
    """
    if not speech_chunks:
        return ""

    full_transcription = ""
    sample_rate = 16000

    for chunk in speech_chunks:
        start_sample = int(chunk["start"] / 1000 * sample_rate)
        end_sample = int(chunk["end"] / 1000 * sample_rate)
        audio_segment = audio[start_sample:end_sample]

        if len(audio_segment) > 0:
            input_features = processor(audio_segment, sampling_rate=sample_rate, return_tensors="pt").input_features

            # Generate token ids
            predicted_ids = model.generate(input_features)

            # Decode token ids to text
            transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
            full_transcription += transcription + " "

    return full_transcription.strip()

def normalize_text(text: str) -> str:
    """
    Advanced text normalization for multilingual ASR, especially for Arabic dialects.
    """
    # Lowercase the text
    text = text.lower()

    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # Normalize whitespace to a single space
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove Arabic diacritics
    text = re.sub(r'[\u064B-\u0652]', '', text)

    # Normalize Arabic characters to their basic forms
    text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
    text = text.replace('ة', 'ه')
    text = text.replace('ى', 'ي')

    return text
