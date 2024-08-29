import pyarrow as pa
from pathlib import Path
import pandas as pd
from datasets import load_dataset, Dataset, DatasetDict
import os
import csv
from PIL import Image
import pyewts
from bdrc import get_instance_info

work_info = {}

converter = pyewts.pyewts()

print(os.environ.get('HF_HOME'))

def get_data_df(csv_file, group):
    texts = []
    curr_info = {}
    csv_data = pd.read_csv(csv_file)
    for _, row in csv_data.iterrows():
        work_id = row['work_id']
        if work_id not in work_info.keys():
            curr_info = get_instance_info(f"M{work_id}")
            if curr_info:
                work_info.update(curr_info)
                curr_info = {}
        script = work_info[work_id]['script']
        print_method = work_info[work_id]['printMethod']
        filename = row['image_name']
        label = row['text']
        image_url = get_image_url(filename)
        char_len = len(label)
        texts.append((filename, label, image_url, work_id, char_len, script, print_method))
    df = pd.DataFrame(texts, columns=['filename', 'label', 'url', 'work_id', 'char_len', 'script', 'print_method'])
    return df
    

def create_parquet(train_df):
    train_df.to_parquet('train.parquet', engine='pyarrow')

    # Step 3: Load the Parquet files as Hugging Face datasets
    train_dataset = Dataset.from_pandas(pd.read_parquet('train.parquet'))

    # Step 4: Combine them into a DatasetDict
    dataset_dict = DatasetDict({
        'train': train_dataset,
    })

    dataset_dict.push_to_hub(repo_id='Norbuketaka_datasets', token=os.environ.get('HF_HOME'))

def get_image_url(image_name):
    new_url = f"https://s3.amazonaws.com/monlam.ai.ocr/OCR/training_images/{image_name}"
    return new_url


def get_image_dimension(group, image_name):
    # if group == "derge_tenjur":
    #     image_path = f"/Users/tashitsering/Desktop/lines/{group}/{image_name}"
    # else:
    #     image_path = f"./data/{group}/lines/{group}/{image_name}"
    image_path = f"/Users/tashitsering/Desktop/nobuketaka_numbers/lines/{image_name}"
    if Path(image_path).exists:
        try:
            with Image.open(image_path) as im:
                size = im.size
            return size
        except:
            print(f'image not found {image_name}')
            return None
    else:
        print(image_name)
        return None


def write_csv(csv_list, csv_file):
    with open(csv_file, mode='w', newline='') as file:
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(csv_list)




if __name__ == "__main__":
    data_df = get_data_df(csv_file="/Users/tashitsering/Desktop/.csv", group='lithang_kanjur')
    create_parquet(data_df)
    # group = "derge_tenjur"
    # main(group)
