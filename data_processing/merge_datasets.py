
import pandas as pd
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(file1, file2, output_file):
    """Merges two CSV files into a single file using a robust pandas method."""
    logging.info(f"Starting merge process for {file1} and {file2}")

    try:
        # Reading CSVs with pandas, which is more robust and provides warnings for bad lines.
        # The 'python' engine is required for the on_bad_lines parameter.
        logging.info(f"Reading {file1}...")
        df1 = pd.read_csv(file1, on_bad_lines='warn', engine='python')
        logging.info(f"Finished reading {file1}. Shape: {df1.shape}")

        logging.info(f"Reading {file2}...")
        df2 = pd.read_csv(file2, on_bad_lines='warn', engine='python')
        logging.info(f"Finished reading {file2}. Shape: {df2.shape}")

        # Concatenate the dataframes
        logging.info("Concatenating dataframes...")
        df = pd.concat([df1, df2], ignore_index=True)
        logging.info(f"Concatenated dataframe shape: {df.shape}")

        # Save the merged dataframe
        logging.info(f"Saving merged file to {output_file}...")
        df.to_csv(output_file, index=False)
        logging.info(f"Successfully merged and saved data to {output_file}")

    except FileNotFoundError as e:
        logging.error(f"Error: {e}. Please check the file paths.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge two CSV files.")
    parser.add_argument("file1", help="Path to the first input CSV file.")
    parser.add_argument("file2", help="Path to the second input CSV file.")
    parser.add_argument("output_file", help="Path to the output CSV file.")
    args = parser.parse_args()
    main(args.file1, args.file2, args.output_file)
