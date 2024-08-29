from pathlib import Path
import csv

def get_images():
    images = []
    csv_path = Path(f"./data/csv/batch19-batch28.csv")
    with open(csv_path, mode='r') as file:
        csv_reader = csv.reader(file)
        csv_list = list(csv_reader)
        for row in csv_list[1:]:
            batch_id = row[4]
            if batch_id in ['batch19','batch20', 'batch21', 'batch22']:
                image_name = row[0]
                images.append(image_name)
    return images


def get_new_data(images):
    new_data = []
    for batch_path in Path('/Users/tashitsering/Desktop/batch19-22/').iterdir():
        with open(batch_path, mode='r') as file:
            csv_reader = csv.reader(file)
            csv_list = list(csv_reader)
            for row in csv_list[1:]:
                image_name = row[0]
                if image_name not in images:
                    state = row[2]
                    image_url = row[6]
                    batch_id = row[13]
                    if state == 'accepted':
                        transcript = row[5]
                    elif state == 'finalised':
                        transcript = row[14]
                    new_data.append([image_name, transcript, image_url, state, batch_id])
    return new_data


def write_csv(csv_list, csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_list)

def main():
    images = get_images()
    new_data = get_new_data(images)
    write_csv(new_data, './new_batch19-22.csv')
                            



if __name__ == "__main__":
    main()