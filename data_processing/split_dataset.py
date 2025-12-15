
import pandas as pd
from sklearn.model_selection import train_test_split
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def split_dataset(input_path, train_path, test_path, test_size=0.2, random_state=42):
    """
    Splits a CSV dataset into training and testing sets.

    Args:
        input_path (str): Path to the input CSV file.
        train_path (str): Path to save the training set.
        test_path (str): Path to save the testing set.
        test_size (float): The proportion of the dataset to allocate to the test split.
        random_state (int): The seed used by the random number generator.
    """
    logging.info(f"Reading dataset from {input_path}...")
    try:
        df = pd.read_csv(input_path)

        logging.info(f"Splitting the dataset with test size: {test_size}")
        train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)

        logging.info(f"Saving training set to {train_path}...")
        train_df.to_csv(train_path, index=False)

        logging.info(f"Saving testing set to {test_path}...")
        test_df.to_csv(test_path, index=False)

        logging.info("Dataset splitting complete.")

    except FileNotFoundError:
        logging.error(f"Error: The file at {input_path} was not found.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Split a dataset into training and testing sets.")
    parser.add_argument("input_path", help="Path to the input CSV file.")
    parser.add_argument("train_path", help="Path to save the training set.")
    parser.add_argument("test_path", help="Path to save the testing set.")
    parser.add_argument("--test-size", type=float, default=0.2, help="The proportion of the dataset to allocate to the test split.")
    parser.add_argument("--random-state", type=int, default=42, help="The seed used by the random number generator.")
    args = parser.parse_args()

    split_dataset(args.input_path, args.train_path, args.test_path, args.test_size, args.random_state)
