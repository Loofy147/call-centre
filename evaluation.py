
import argparse
import pandas as pd
from jiwer import wer, cer

def evaluate_asr(predictions_file, ground_truth_file, report_path):
    """
    Evaluates ASR performance by calculating WER, CER, and generating a detailed report.

    Args:
        predictions_file (str): Path to the file containing predicted transcriptions.
        ground_truth_file (str): Path to the file containing ground truth transcriptions.
        report_path (str): Path to save the detailed evaluation report.
    """
    with open(predictions_file, 'r', encoding='utf-8') as f:
        predictions = [line.strip() for line in f]

    with open(ground_truth_file, 'r', encoding='utf-8') as f:
        ground_truth = [line.strip() for line in f]

    if len(predictions) != len(ground_truth):
        raise ValueError("The number of predictions and ground truth lines do not match.")

    # Calculate overall metrics
    overall_wer = wer(ground_truth, predictions)
    overall_cer = cer(ground_truth, predictions)

    print(f"Overall Word Error Rate (WER): {overall_wer:.4f}")
    print(f"Overall Character Error Rate (CER): {overall_cer:.4f}")

    # Generate a detailed report
    report_data = []
    for i in range(len(predictions)):
        report_data.append({
            'Ground Truth': ground_truth[i],
            'Prediction': predictions[i],
            'WER': wer(ground_truth[i], predictions[i]),
            'CER': cer(ground_truth[i], predictions[i])
        })

    report_df = pd.DataFrame(report_data)
    report_df.to_csv(report_path, index=False)

    print(f"Detailed evaluation report saved to {report_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Evaluate ASR performance.")
    parser.add_argument("predictions_file", help="Path to the file with predicted transcriptions.")
    parser.add_argument("ground_truth_file", help="Path to the file with ground truth transcriptions.")
    parser.add_argument("--report-path", default="evaluation_report.csv", help="Path to save the detailed report.")
    args = parser.parse_args()

    evaluate_asr(args.predictions_file, args.ground_truth_file, args.report_path)
