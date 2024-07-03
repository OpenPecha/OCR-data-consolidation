from pathlib import Path
from datasets import load_dataset, Dataset, DatasetDict
import os
import pandas as pd

lithang_name_updated = Path('./data/lithang_kanjur/lithang_name_changed.txt').read_text().splitlines()


def get_combined_list(list_paths):
    new_list = []
    for list_path in list_paths:
        image_list = (Path(list_path).read_text()).splitlines()
        for image in image_list:
            if image in lithang_name_updated:
                new_name = 'LIKA_'+ image + '.jpg'
            else:
                new_name = image + '.jpg' 
            new_list.append(new_name)
    return new_list

def get_split(train_images, test_images, eval_images):
    combined_dataset = load_dataset('ta4tsering/Lhasa_kanjur_datasets')
    combined_df = combined_dataset['train'].to_pandas()
    train_df = combined_df[combined_df['filename'].isin(train_images)]
    test_df = combined_df[combined_df['filename'].isin(test_images)]
    eval_df = combined_df[combined_df['filename'].isin(eval_images)]
    create_parquet(train_df, test_df, eval_df)


def create_parquet(train_df, test_df, eval_df):
    train_df.to_parquet('train.parquet', engine='pyarrow')
    eval_df.to_parquet('eval.parquet', engine='pyarrow')
    test_df.to_parquet('test.parquet', engine='pyarrow')

    # Step 3: Load the Parquet files as Hugging Face datasets
    train_dataset = Dataset.from_pandas(pd.read_parquet('train.parquet'))
    eval_dataset = Dataset.from_pandas(pd.read_parquet('eval.parquet'))
    test_dataset = Dataset.from_pandas(pd.read_parquet('test.parquet'))

    # Step 4: Combine them into a DatasetDict
    dataset_dict = DatasetDict({
        'train': train_dataset,
        'eval': eval_dataset,
        'test': test_dataset
    })

    dataset_dict.push_to_hub(repo_id='Woodblock_datasets_with_split', token=os.environ.get('HF_HOME'))


def main():
    lhasa_dir = './data/lhasa_kanjur'
    lithang_dir = './data/lithang_kanjur'
    derge_dir = './data/derge_tenjur'
    test_paths = [f'{lhasa_dir}/test_imgs.txt', f'{lithang_dir}/test_imgs.txt', f'{derge_dir}/test_imgs.txt']
    eval_paths = [f'{lhasa_dir}/eval_imgs.txt', f'{lithang_dir}/eval_imgs.txt', f'{derge_dir}/eval_imgs.txt']
    train_paths = [f'{lhasa_dir}/train_imgs.txt', f'{lithang_dir}/train_imgs.txt', f'{derge_dir}/train_imgs.txt']
    test_images = get_combined_list(test_paths)
    eval_images = get_combined_list(eval_paths)
    train_images = get_combined_list(train_paths)
    get_split(train_images, test_images, eval_images)





if __name__ == "__main__":
    main()
