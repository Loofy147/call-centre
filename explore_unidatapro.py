
from datasets import load_dataset

# Load the dataset
arabic_speech_dataset = load_dataset("UniDataPro/arabic-speech-recognition")

# Print the dataset information
print(arabic_speech_dataset)

# Inspect the features of the 'train' split
print(arabic_speech_dataset['train'].features)

# Inspect the first example
print(arabic_speech_dataset['train'][0])
