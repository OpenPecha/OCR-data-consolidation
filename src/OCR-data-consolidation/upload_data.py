from pathlib import Path
import os

def copy_images(images_list):
    image_dirs = Path(f'./data/lhasa_kangyur/').iterdir()
    for image_dir in image_dirs:
        image_paths = image_dir.iterdir()
        for image_path in image_paths:
            image_name = image_path.name
            if image_name in images_list:
                os.system(f'cp {image_path} ./data/OCR/training_images/{image_name}')


def get_images_names():
    final_list = []
    list_paths = list(Path('./data/lhasa_kanjur/transcriptions/').iterdir())
    for list_path in list_paths:
        images = list_path.read_text().split('\n')
        final_list.extend(images)
    return final_list


def main():
    images_list = get_images_names()
    copy_images(images_list)


if __name__ == '__main__':
    main()