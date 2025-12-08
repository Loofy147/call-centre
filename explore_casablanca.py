
from datasets import load_dataset, concatenate_datasets

# Load the Algerian subset of the Casablanca dataset
casablanca_dataset = load_dataset("UBC-NLP/Casablanca", "Algeria")

# Combine the validation and test splits into a single training set
train_dataset = concatenate_datasets([casablanca_dataset['validation'], casablanca_dataset['test']])

# Create a new test split
train_test_split = train_dataset.train_test_split(test_size=0.1)
train_dataset = train_test_split['train']
test_dataset = train_test_split['test']

# Print the dataset information
print("Train dataset:", train_dataset)
print("Test dataset:", test_dataset)


# Inspect the features of the 'train' split
print(train_dataset.features)

# Inspect the first example
print(train_dataset[0])
