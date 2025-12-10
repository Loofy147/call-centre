import pandas as pd

df = pd.read_excel('asr_starter_repo/data/AlgD_Toxicity_Speech_Dataset.xlsx')
with open('asr_starter_repo/data/comments.txt', 'w', encoding='utf-8') as f:
    for comment in df['comment']:
        f.write(comment + '\n')
