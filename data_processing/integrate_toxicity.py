
import pandas as pd
import argparse
import csv

def main(merged_dataset_path, comments_file_path, final_dataset_path):
    """Integrates toxic comments into the merged dataset."""
    # Read the merged dataset using the csv module
    with open(merged_dataset_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = list(reader)

    # Convert the data to a DataFrame, handling potential extra columns
    df = pd.DataFrame(data)
    df = df.iloc[:, :len(header)]
    df.columns = header

    # Read the toxic comments
    with open(comments_file_path, 'r', encoding='utf-8') as f:
        toxic_comments = [line.strip() for line in f]

    # Create new rows for each toxic comment
    new_rows = []
    for i, comment in enumerate(toxic_comments):
        new_rows.append({
            'ID': f'TOX-{i+1:03d}',
            'Sector': 'General',
            'Topic': 'Toxic Comment',
            'Customer_Query_AR': comment,
            'Customer_Query_FR': '',  # No translation available
            'Customer_Query_EN': '',  # No translation available
            'Agent_Response_AR': 'نعتذر عن الإزعاج، سيتم مراجعة هذا التعليق.',
            'Agent_Response_FR': 'Nous nous excusons pour le désagrément, ce commentaire sera examiné.',
            'Agent_Action': 'Flag for review',
            'Sentiment': 'Toxic'
        })

    # Convert the list of dictionaries to a DataFrame
    new_rows_df = pd.DataFrame(new_rows)

    # Append the new rows to the original DataFrame
    df = pd.concat([df, new_rows_df], ignore_index=True)

    # Save the final dataset
    df.to_csv(final_dataset_path, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Integrate toxic comments into a dataset.")
    parser.add_argument("merged_dataset_path", help="Path to the merged dataset CSV file.")
    parser.add_argument("comments_file_path", help="Path to the text file containing toxic comments.")
    parser.add_argument("final_dataset_path", help="Path to the output CSV file.")
    args = parser.parse_args()
    main(args.merged_dataset_path, args.comments_file_path, args.final_dataset_path)
