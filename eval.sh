#!/usr/bin/env bash
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <prediction> <ground_truth_file>"
  exit 1
fi
prediction="$1"
ground_truth_file="$2"
python -c '
import sys
from jiwer import wer
prediction = sys.argv[1]
ground_truth_file = sys.argv[2]
with open(ground_truth_file, "r", encoding="utf-8") as f:
    ground_truth = f.read()
print("WER:", wer(ground_truth, prediction))
' "$prediction" "$ground_truth_file"
