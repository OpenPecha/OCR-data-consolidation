import pyarrow as pa
from pathlib import Path
import pandas as pd
from datasets import load_dataset, Dataset, DatasetDict
import os
import csv
from PIL import Image
import pyewts


converter = pyewts.pyewts()

print(os.environ.get('HF_HOME'))

def get_data_df(csv_file, group):
    all_images = (Path(f"./data/{group}/all_images.txt").read_text()).splitlines()
    texts = []
    csv_data = pd.read_csv(csv_file)
    for _, row in csv_data.iterrows():
        filename = row['image_name']
        label = row['label']
        image_url = row['image_url']
        char_len = row['char_len']
        # dimension = row['dimension']
        work_id = row['work_id']
        script = row['script']
        print_method = row['print_method']
        texts.append((filename, label, image_url, char_len, work_id, script, print_method))
    df = pd.DataFrame(texts, columns=['filename', 'label', 'url', 'char_len', 'work_id', 'script', 'print_method'])
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
    if group == "derge_tenjur":
        image_path = f"/Users/tashitsering/Desktop/Work/hugging_face/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/hub/datasets--Eric-23xd--DergeTenjur/snapshots/012d522bbc301ec26679eecb06b18935533ee896/lines/{image_name}"
    else:
        image_path = f"./data/{group}/lines/{image_name}"
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


def main(group):
    csv_list = []
    transcript_paths = list(Path(f"./data/{group}/transcriptions/").iterdir())
    for transcript_path in transcript_paths:
        transcript = converter.toUnicode(transcript_path.read_text(encoding='utf-8'))
        image_name = transcript_path.stem + ".jpg"
        image_url = get_image_url(image_name)
        char_len = len(transcript)
        image_dimension = get_image_dimension(group, image_name)
        if image_dimension == None:
            continue
        script = "Uchan"
        print_method = "WoodBlock"
        curr_csv = [image_name, transcript, image_url, char_len, image_dimension, script, print_method]
        csv_list.append(curr_csv)
        curr_csv = []
    csv_file = Path(f"./data/csv/{group}.csv")
    write_csv(csv_list, csv_file)
    # data_df = get_data_df(csv_file)






if __name__ == "__main__":
    data_df = get_data_df(csv_file="./norbuketaka.csv", group='lithang_kanjur')
    create_parquet(data_df)
    # group = "derge_tenjur"
    # main(group)
