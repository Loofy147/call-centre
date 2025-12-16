
import pandas as pd
from gtts import gTTS
import os
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_audio_dataset(input_path, output_dir, limit=None):
    """
    Generates an audio dataset from a CSV file containing text.

    Args:
        input_path (str): Path to the input CSV file.
        output_dir (str): Directory to save the audio files and the new CSV.
        limit (int, optional): The number of samples to generate. Defaults to None.
    """
    logging.info(f"Reading dataset from {input_path}...")
    try:
        df = pd.read_csv(input_path)

        if limit:
            df = df.head(limit)

        audio_dir = os.path.join(output_dir, "audio")
        os.makedirs(audio_dir, exist_ok=True)

        new_data = []

        for index, row in df.iterrows():
            text = row['Customer_Query_AR']
            audio_filename = f"audio_{index}.mp3"
            audio_path = os.path.join(audio_dir, audio_filename)

            try:
                tts = gTTS(text=text, lang='ar')
                tts.save(audio_path)

                new_data.append({
                    'audio_path': audio_path,
                    'transcription': text
                })

                logging.info(f"Generated audio for row {index}")

            except Exception as e:
                logging.error(f"Error generating audio for row {index}: {e}")

        new_df = pd.DataFrame(new_data)
        new_df.to_csv(os.path.join(output_dir, "audio_dataset.csv"), index=False)

        logging.info("Audio dataset generation complete.")

    except FileNotFoundError:
        logging.error(f"Error: The file at {input_path} was not found.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate an audio dataset from a CSV file.")
    parser.add_argument("input_path", help="Path to the input CSV file.")
    parser.add_argument("output_dir", help="Directory to save the audio files and the new CSV.")
    parser.add_argument("--limit", type=int, default=None, help="The number of samples to generate.")
    args = parser.parse_args()

    generate_audio_dataset(args.input_path, args.output_dir, args.limit)
