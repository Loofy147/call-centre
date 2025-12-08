
import torch
from datasets import load_from_disk
from transformers import (
    WhisperForConditionalGeneration,
    WhisperFeatureExtractor,
    WhisperTokenizer,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    WhisperProcessor,
)

try:
    print("Starting the fine-tuning script...")

    # Load the preprocessed datasets
    print("Loading datasets...")
    train_dataset = load_from_disk("asr_starter_repo/data/train_dataset")
    test_dataset = load_from_disk("asr_starter_repo/data/test_dataset")
    print("Datasets loaded successfully.")

    # Load the Whisper model, feature extractor, and tokenizer
    print("Loading model, feature extractor, and tokenizer...")
    model_name = "openai/whisper-base"
    feature_extractor = WhisperFeatureExtractor.from_pretrained(model_name)
    tokenizer = WhisperTokenizer.from_pretrained(model_name, language="arabic", task="transcribe")
    processor = WhisperProcessor.from_pretrained(model_name, language="arabic", task="transcribe")
    model = WhisperForConditionalGeneration.from_pretrained(model_name)
    print("Model, feature extractor, and tokenizer loaded successfully.")


    # Data collator
    class DataCollatorSpeechSeq2SeqWithPadding:
        def __init__(self, processor):
            self.processor = processor

        def __call__(self, features):
            input_features = [{"input_features": feature["input_features"]} for feature in features]
            batch = self.processor.feature_extractor.pad(input_features, return_tensors="pt")

            label_features = [{"input_ids": feature["labels"]} for feature in features]
            labels_batch = self.processor.tokenizer.pad(label_features, return_tensors="pt")

            labels = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)

            if (labels[:, 0] == self.processor.tokenizer.bos_token_id).all().cpu().item():
                labels = labels[:, 1:]

            batch["labels"] = labels

            return batch

    data_collator = DataCollatorSpeechSeq2SeqWithPadding(processor=processor)

    # Prepare the dataset for training
    print("Preparing dataset for training...")
    def prepare_dataset(batch):
        audio = batch["audio"]
        batch["input_features"] = feature_extractor(audio["array"], sampling_rate=audio["sampling_rate"]).input_features[0]
        batch["labels"] = tokenizer(batch["sentence"]).input_ids
        return batch

    train_dataset = train_dataset.map(prepare_dataset, remove_columns=train_dataset.column_names)
    test_dataset = test_dataset.map(prepare_dataset, remove_columns=test_dataset.column_names)
    print("Dataset prepared successfully.")


    # Training arguments
    training_args = Seq2SeqTrainingArguments(
        output_dir="./asr_starter_repo/models/whisper-base-ar-finetuned",
        per_device_train_batch_size=8,
        gradient_accumulation_steps=1,
        learning_rate=1e-5,
        warmup_steps=50,
        num_train_epochs=3,
        eval_strategy="epoch",
        fp16=True,
    )

    # Trainer
    trainer = Seq2SeqTrainer(
        args=training_args,
        model=model,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        data_collator=data_collator,
        tokenizer=processor.feature_extractor,
    )

    # Start training
    print("Starting training...")
    trainer.train()
    print("Training complete.")

    # Save the model
    print("Saving model...")
    model.save_pretrained("./asr_starter_repo/models/whisper-base-ar-finetuned")
    print("Model saved successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
