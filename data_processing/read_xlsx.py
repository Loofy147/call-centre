
import pandas as pd
import argparse

def main(input_path, output_path):
    """Reads comments from an xlsx file and writes them to a text file."""
    df = pd.read_excel(input_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        for comment in df['comment']:
            f.write(comment + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract comments from an XLSX file.")
    parser.add_argument("input_path", help="Path to the input XLSX file.")
    parser.add_argument("output_path", help="Path to the output text file.")
    args = parser.parse_args()
    main(args.input_path, args.output_path)
