#!/usr/bin/env bash

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <model-name> <audio-file> <ground-truth-file>"
  exit 1
fi

MODEL_NAME=$1
AUDIO_FILE=$2
GROUND_TRUTH_FILE=$3

# Install dependencies
pip install jiwer librosa webrtcvad

# Run inference
python asr_starter_repo/inference.py --model-name "$MODEL_NAME" --audio-file "$AUDIO_FILE"

# Calculate WER
python - "transcript.json" "$GROUND_TRUTH_FILE" <<'PY'
import json,sys
from jiwer import wer
with open(sys.argv[1],'r',encoding='utf-8') as f:
    j=json.load(f)
pred=j.get('text','')
with open(sys.argv[2],'r',encoding='utf-8') as f:
    gt=f.read()
print('WER:', wer(gt, pred))
PY
