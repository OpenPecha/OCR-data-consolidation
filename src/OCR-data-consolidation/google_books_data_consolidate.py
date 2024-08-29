from pathlib import Path
import csv
from PIL import Image
import subprocess
import os
from bdrc import get_instance_info


google_books_line_dir = "./data/google_books_lines/"
final_csv = []
work_info = {}


def convert_tiff_to_jpg(input_path, image_name, quality=85):
    output_path = Path(google_books_line_dir) / (image_name.split('.')[0]+".jpg")
    with Image.open(input_path) as img:
        img = img.convert("RGB")
        img.save(output_path, "JPEG", quality=quality)


def copy_image_to_line_dir(image_path):
    image_name = image_path.name
    if image_name.split(".")[-1] in ['tif', 'tiff']:
        convert_tiff_to_jpg(image_path, image_name)
    else:
        subprocess.run(['cp', image_path, google_books_line_dir])


def gather_line_images(work_paths):
    for work_path in work_paths:
        line_image_paths = list((work_path / "images").iterdir())
        for line_image_path in line_image_paths:
            image_name = (line_image_path.stem)+".jpg"
            image_path = Path(google_books_line_dir) / image_name
            if image_path.exists():
                continue
            copy_image_to_line_dir(line_image_path)


def get_new_image_name(image_name):
    if image_name.split(".")[-1] in ['tif', 'tiff']:
        new_image_name = image_name.split(".")[0] + ".jpg"
    else:
        new_image_name = image_name
    return new_image_name


def get_image_dimension(image_name):
    image_path = Path(f"./data/google_books_lines/{image_name}")
    if image_path.exists:
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


def consolidate_csv(csv_path):
    with open(csv_path, mode ='r')as file:
        csvFile = list(csv.reader(file))
        for line in csvFile[1:]:
            work_id = line[0]
            image_name = get_new_image_name(line[-3])
            transcript = line[5]
            image_url = "https://s3.amazonaws.com/monlam.ai.ocr/OCR/training_images/" + image_name
            char_len = len(transcript)
            dimension = get_image_dimension(image_name)
            if work_info[work_id]:
                try:
                    script = work_info[work_id]['script'][0]
                except:
                    script = None
                print_method = work_info[work_id]['printMethod'][0]
            else:
                script = None
                print_method = None
            final_csv.append([image_name, transcript, image_url, char_len, dimension, work_id, script, print_method])


def gather_csv(work_paths):
    for work_path in work_paths:
        work_id = work_path.stem
        csv_path = work_path / (work_id+".csv")
        consolidate_csv(csv_path)

def get_work_info(work_paths):
    curr_info = {}
    for work_path in work_paths:
        work_id = work_path.name
        curr_info = get_instance_info(f"M{work_id}")
        if curr_info:
            work_info.update(curr_info)
            curr_info = {}

def write_csv():
    with open("./google_books.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(final_csv)

def main():
    work_paths = list(Path(f'./data/google_books/').iterdir())
    get_work_info(work_paths)
    # gather_line_images(work_paths)
    gather_csv(work_paths)
    write_csv()


if __name__ == "__main__":
    main()