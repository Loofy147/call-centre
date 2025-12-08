
import csv

def merge_csv_files(file1, file2, output_file):
    with open(file1, 'r', encoding='utf-8') as f1, \
         open(file2, 'r', encoding='utf-8') as f2, \
         open(output_file, 'w', encoding='utf-8', newline='') as fout:

        reader1 = csv.reader(f1)
        reader2 = csv.reader(f2)
        writer = csv.writer(fout)

        # Write header from the first file
        header = next(reader1)
        writer.writerow(header)

        # Skip header in the second file
        next(reader2)

        # Write data from the first file
        for row in reader1:
            writer.writerow(row)

        # Write data from the second file
        for row in reader2:
            writer.writerow(row)

if __name__ == "__main__":
    merge_csv_files(
        'asr_starter_repo/data/algerian_call_center_dataset.csv',
        'asr_starter_repo/data/new_commercial_entries.csv',
        'asr_starter_repo/data/merged_dataset.csv'
    )
