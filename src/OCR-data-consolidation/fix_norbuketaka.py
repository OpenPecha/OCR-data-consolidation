from pathlib import Path
import csv


def read_csv(csv_file):
    with open(csv_file, mode='r') as file:
        csv_reader = csv.reader(file)
        csv_list = list(csv_reader)
    return csv_list

def get_set(norbuketaka_csv):
    imagenames = []
    for row in norbuketaka_csv[1:]:
        image_name = row[1]
        # if image_name in imagenames:
        #     continue
        # else:
        imagenames.append(image_name)
    return imagenames


def get_new_csv(norbuketaka_csv, image_names):
    new_csv = []
    repeated = []
    done_list = []
    for row in norbuketaka_csv[1:]:
        image_name = row[1]
        if image_name in done_list:
            repeated.append(image_name)
            continue
        elif image_name in image_names:
            image_name = row[1]
            work_id = row[0].split('/')[0]
            transcript = row[3]
            new_csv.append([work_id, image_name, transcript])
            done_list.append(image_name)
    write_csv(new_csv, "repeated_images.csv")
    return new_csv

def get_image_names():
    image_names = []
    for dir_path in Path(f"/Users/tashitsering/Desktop/Norbuketaka/").iterdir():
        for image_path in dir_path.iterdir():
            image_name = image_path.name
            image_names.append(image_name)
    return set(image_names)

def write_csv(new_csv, file_name):
    with open(f"./{file_name}", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(new_csv)


def main():
    image_names = get_image_names()
    norbuketaka_path = Path(f"./data/csv/norbuketaka.csv")
    norbuketaka_csv = read_csv(norbuketaka_path)
    new_csv = get_new_csv(norbuketaka_csv, image_names)
    write_csv(new_csv, "norbuketaka_filtered.csv")

if __name__ == "__main__":
    main() 