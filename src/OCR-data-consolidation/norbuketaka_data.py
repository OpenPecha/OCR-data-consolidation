from pathlib import Path
import csv
from PIL import Image
import subprocess
import os
from bdrc import get_instance_info


final_csv = []
work_info = {}


def update_csv(csv_path):
    curr_info = {}
    with open(csv_path, mode ='r')as file:
        csvFile = list(csv.reader(file))
        for line in csvFile[1:]:
            work_id = line[0].split("/")[0]
            image_name = line[1]
            transcript = line[3]
            image_url = "https://s3.amazonaws.com/monlam.ai.ocr/OCR/training_images/" + image_name
            char_len = len(transcript)
            if len(work_info.keys()) == 0:
                curr_info = get_instance_info(f"M{work_id}")
                work_info.update(curr_info)
                curr_info = {}
            elif work_id not in work_info.keys():
                curr_info = get_instance_info(f"M{work_id}")
                work_info.update(curr_info)
                curr_info = {}
            script = work_info[work_id]['script'][0]
            print_method = work_info[work_id]['printMethod'][0]
            final_csv.append([image_name, transcript, image_url, char_len, work_id, script, print_method])


def write_csv():
    with open("./norbuketaka.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(final_csv)


def main():
    update_csv(csv_path="./data/csv/norbuketaka.csv")
    write_csv()


if __name__ == "__main__":
    main()