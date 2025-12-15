
import argparse
import pandas as pd
import asyncio
from src.asr_agent_integration import VoiceAgentPipeline, load_config
import os

async def run_evaluation(model_name, test_dataset_path, output_dir, limit=None):
    """
    Runs the ASR model evaluation pipeline.

    Args:
        model_name (str): The name of the ASR model to evaluate.
        test_dataset_path (str): Path to the test dataset CSV file.
        output_dir (str): Directory to save the evaluation results.
        limit (int, optional): The number of samples to evaluate. Defaults to None.
    """
    config = load_config()
    config['asr_model']['name'] = model_name

    pipeline = VoiceAgentPipeline(config=config)

    test_df = pd.read_csv(test_dataset_path)

    if limit:
        test_df = test_df.head(limit)

    predictions = []
    ground_truths = []

    for index, row in test_df.iterrows():
        # Assuming the dataset has 'audio_path' and 'transcription' columns
        audio_path = row['audio_path']
        ground_truth = row['transcription']

        if not os.path.exists(audio_path):
            print(f"Warning: Audio file not found at {audio_path}. Skipping.")
            continue

        result = await pipeline.process_voice_call(audio_path=audio_path, customer_id=f"eval_{index}")

        predictions.append(result['transcription']['text'])
        ground_truths.append(ground_truth)

    # Save predictions and ground truths to files
    predictions_path = os.path.join(output_dir, "predictions.txt")
    ground_truth_path = os.path.join(output_dir, "ground_truth.txt")
    report_path = os.path.join(output_dir, f"{model_name.replace('/', '_')}_evaluation_report.csv")

    with open(predictions_path, 'w', encoding='utf-8') as f:
        for pred in predictions:
            f.write(pred + '\n')

    with open(ground_truth_path, 'w', encoding='utf-8') as f:
        for gt in ground_truths:
            f.write(gt + '\n')

    # Run the evaluation script
    from evaluation import evaluate_asr
    evaluate_asr(predictions_path, ground_truth_path, report_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run ASR model evaluation.")
    parser.add_argument("--model-name", type=str, default="openai/whisper-small", help="The name of the ASR model to evaluate.")
    parser.add_argument("--test-dataset-path", type=str, default="data/audio_dataset/audio_dataset.csv", help="Path to the test dataset CSV file.")
    parser.add_argument("--output-dir", type=str, default="evaluation_results", help="Directory to save the evaluation results.")
    parser.add_argument("--limit", type=int, default=None, help="The number of samples to evaluate.")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    asyncio.run(run_evaluation(args.model_name, args.test_dataset_path, args.output_dir, args.limit))
