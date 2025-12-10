# Algerian Call Center ASR

This repository provides a comprehensive solution for Automatic Speech Recognition (ASR) tailored for Algerian call centers. It includes a data processing pipeline for creating a comprehensive dataset and an ASR inference module using Hugging Face's Whisper model.

## Project Structure

- `data/`: Contains the raw and processed datasets.
- `data_processing/`: Contains scripts for cleaning, merging, and preparing the data.
- `Dockerfile`: For containerizing the application.
- `eval.sh`: A script for evaluating the ASR model's performance.
- `inference.py`: The main script for running ASR inference.
- `requirements.txt`: A list of Python dependencies.

## Usage

### 1. Data Processing

To create the comprehensive Algerian call center dataset, run the following command:

```bash
python -m data_processing.main
```

This will run the entire data processing pipeline and generate the final dataset in the `data` directory.

### 2. ASR Inference

To run ASR inference on an audio file, use the following command:

```bash
python inference.py --audio-file <path/to/audio/file>
```

The transcribed text will be printed to standard output.

### 3. Evaluation

To evaluate the ASR model's performance, you can pass the output of the inference script to the `eval.sh` script:

```bash
./eval.sh "$(python inference.py --audio-file sample_audio.wav)" ground_truth.txt
```

This will calculate and print the Word Error Rate (WER) of the transcription.

### Docker

To build and run the application in a Docker container, use the following commands:

1.  **Build the Docker image:**

    ```bash
    docker build -t algerian-asr .
    ```

2.  **Run the Docker container:**

    ```bash
    docker run algerian-asr
    ```

This will run the inference script on the sample audio file with the default model.
