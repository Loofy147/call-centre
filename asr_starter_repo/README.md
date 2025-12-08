# ASR Starter Repo

This repository provides a starter kit for running automatic speech recognition (ASR) inference using Hugging Face models. It includes a Python script for transcription, a Dockerfile for containerization, and a sample audio file for testing.

## Usage

### Local Python Environment

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run inference:**
   ```bash
   python inference.py --model-name <model-name> --audio-file <audio-file>
   ```

### Docker

1. **Build the Docker image:**
   ```bash
   docker build -t asr-starter .
   ```

2. **Run the Docker container:**
   ```bash
   docker run asr-starter
   ```
   This will run the inference script on the sample audio file with the default model.
