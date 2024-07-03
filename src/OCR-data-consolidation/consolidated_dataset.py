from datasets import load_dataset, DatasetDict, Dataset
import pandas as pd
import os

# Load datasets
lhasa_dataset = load_dataset('ta4tsering/Lhasa_kanjur_datasets')
lhasa_train_df = lhasa_dataset['train'].to_pandas()

lithang_dataset = load_dataset('ta4tsering/Lithang_Kanjur_datasets')
lithang_train_df = lithang_dataset['train'].to_pandas()

derge_dataset = load_dataset('ta4tsering/Derge_Tenjur_datasets')
derge_train_df = derge_dataset['train'].to_pandas()

# Combine datasets
combined_df = pd.concat([lhasa_train_df, lithang_train_df, derge_train_df], ignore_index=True)

# # Convert back to Dataset
# combined_dataset = Dataset.from_pandas(combined_df)

def create_parquet(train_df):
    train_df.to_parquet('train.parquet', engine='pyarrow')

    # Step 3: Load the Parquet files as Hugging Face datasets
    train_dataset = Dataset.from_pandas(pd.read_parquet('train.parquet'))

    # Step 4: Combine them into a DatasetDict
    dataset_dict = DatasetDict({
        'train': train_dataset,
    })

    dataset_dict.push_to_hub(repo_id='Woodblock_datasets', token=os.environ.get('HF_HOME'))


def main():
    create_parquet(combined_df)

if __name__ == "__main__":
    main()