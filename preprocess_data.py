
from datasets import load_dataset, concatenate_datasets, Audio
import re

def preprocess_casablanca(dataset):
    # Combine validation and test splits
    combined_dataset = concatenate_datasets([dataset['validation'], dataset['test']])

    # Resample audio to 16kHz
    combined_dataset = combined_dataset.cast_column("audio", Audio(sampling_rate=16000))

    # Normalize text
    def normalize_text(batch):
        # Remove punctuation and special characters
        batch["transcription"] = re.sub(r'[^\w\s]', '', batch["transcription"])
        return batch

    combined_dataset = combined_dataset.map(normalize_text)

    # Select and rename columns
    combined_dataset = combined_dataset.rename_column("transcription", "sentence")
    combined_dataset = combined_dataset.select_columns(["audio", "sentence"])

    return combined_dataset

if __name__ == "__main__":
    # Load the Algerian subset of the Casablanca dataset
    casablanca_dataset = load_dataset("UBC-NLP/Casablanca", "Algeria")

    # Preprocess the dataset
    preprocessed_casablanca = preprocess_casablanca(casablanca_dataset)

    # Split into train and test sets
    train_test_split = preprocessed_casablanca.train_test_split(test_size=0.1)
    train_dataset = train_test_split['train']
    test_dataset = train_test_split['test']

    # Save the datasets
    train_dataset.save_to_disk("asr_starter_repo/data/train_dataset")
    test_dataset.save_to_disk("asr_starter_repo/data/test_dataset")

    print("Preprocessing complete.")
    print("Train dataset:", train_dataset)
    print("Test dataset:", test_dataset)
