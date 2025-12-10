
import argparse
from . import read_xlsx, merge_datasets, integrate_toxicity

def main():
    parser = argparse.ArgumentParser(description='Data processing pipeline.')
    parser.add_argument('--xlsx-file', type=str, default='data/AlgD_Toxicity_Speech_Dataset.xlsx', help='Path to the toxicity dataset.')
    parser.add_argument('--comments-file', type=str, default='data/comments.txt', help='Path to the output comments file.')
    parser.add_argument('--call-center-dataset', type=str, default='data/algerian_call_center_dataset.csv', help='Path to the call center dataset.')
    parser.add_argument('--new-entries-dataset', type=str, default='data/new_commercial_entries.csv', help='Path to the new entries dataset.')
    parser.add_argument('--merged-dataset', type=str, default='data/merged_dataset.csv', help='Path to the merged dataset.')
    parser.add_argument('--final-dataset', type=str, default='data/comprehensive_algerian_call_center_dataset.csv', help='Path to the final dataset.')
    args = parser.parse_args()

    # Step 1: Read comments from XLSX
    print('Reading comments from XLSX...')
    read_xlsx.main(args.xlsx_file, args.comments_file)

    # Step 2: Merge datasets
    print('Merging datasets...')
    merge_datasets.main(args.call_center_dataset, args.new_entries_dataset, args.merged_dataset)

    # Step 3: Integrate toxicity
    print('Integrating toxicity...')
    integrate_toxicity.main(args.merged_dataset, args.comments_file, args.final_dataset)

    print('Data processing complete.')

if __name__ == '__main__':
    main()
