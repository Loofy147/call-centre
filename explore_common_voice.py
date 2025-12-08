
from datasets import load_dataset
from huggingface_hub import login

# Login to Hugging Face Hub
login(token="hf_KxRsDivwHxUplWejFeKdsXaOCKERvlZux")

# Load the Arabic subset of the Common Voice dataset
common_voice_dataset = load_dataset("common_voice", "ar")

# Print the dataset information
print(common_voice_dataset)

# Inspect the features of the 'train' split
print(common_voice_dataset['train'].features)

# Inspect the first example
print(common_voice_dataset['train'][0])
