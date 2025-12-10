
import pandas as pd
import argparse
import csv

def read_csv_robust(filepath):
    """Reads a CSV file with potential parsing errors."""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = list(reader)

    # Find the maximum number of columns
    max_cols = 0
    for row in data:
        if len(row) > max_cols:
            max_cols = len(row)

    # Pad rows with fewer columns
    for row in data:
        while len(row) < max_cols:
            row.append('')

    # Pad header if necessary
    while len(header) < max_cols:
        header.append(f'Unnamed: {len(header)}')

    df = pd.DataFrame(data, columns=header)
    return df

def main(file1, file2, output_file):
    """Merges two CSV files into a single file using a robust method."""
    df1 = read_csv_robust(file1)
    df2 = read_csv_robust(file2)

    df = pd.concat([df1, df2], ignore_index=True)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge two CSV files.")
    parser.add_argument("file1", help="Path to the first input CSV file.")
    parser.add_argument("file2", help="Path to the second input CSV file.")
    parser.add_argument("output_file", help="Path to the output CSV file.")
    args = parser.parse_args()
    main(args.file1, args.file2, args.output_file)
