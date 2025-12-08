
import pandas as pd

# Read the merged dataset
df = pd.read_csv('asr_starter_repo/data/merged_dataset.csv')

# Read the toxic comments
with open('asr_starter_repo/data/comments.txt', 'r', encoding='utf-8') as f:
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
df.to_csv('asr_starter_repo/data/comprehensive_algerian_call_center_dataset.csv', index=False)
