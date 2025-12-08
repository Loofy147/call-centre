#!/usr/bin/env bash
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 transcript.json ground_truth.txt"
  exit 1
fi
python - "$1" "$2" <<'PY'
import json,sys
from jiwer import wer
with open(sys.argv[1],'r',encoding='utf-8') as f:
    j=json.load(f)
pred=j.get('text','')
with open(sys.argv[2],'r',encoding='utf-8') as f:
    gt=f.read()
print('WER:', wer(gt, pred))
PY
