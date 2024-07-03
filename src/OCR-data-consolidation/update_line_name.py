from pathlib import Path
import os

def get_same_line_names():
    lhasa_list = Path('./data/lhasa_kanjur/lhasa_images.txt').read_text().split('\n')
    lithang_list = Path('./data/lithang_kanjur/lithang_images.txt').read_text().split('\n')
    derge_list = Path('./data/derge_tenjur/derge_images.txt').read_text().split('\n')
    lhasa_list = set(lhasa_list)
    lithang_list = set(lithang_list)
    if len(lhasa_list.intersection(lithang_list)) == 0:
        uninion_set = lhasa_list.union(lithang_list)
        same_images = uninion_set.intersection(derge_list)
    return list(same_images)

def update_line_names():
    same_images = get_same_line_names()
    image_dirs = Path('./data/derge_tenjur/lines/')
    transcript_dirs = Path('./data/derge_tenjur/transcriptions/')
    for line_image in same_images:
        new_line_name = "DETN_" + line_image
        line_image_path = image_dirs / f"{line_image}.jpg"
        new_line_image_path = image_dirs / f"{new_line_name}.jpg"
        transcript_path = transcript_dirs / f"{line_image}.txt"
        new_transcript_path = transcript_dirs / f"{new_line_name}.txt"
        if line_image_path.exists():
            os.rename(line_image_path, new_line_image_path)
        else:
            print(f"{line_image} image does not exist")
        if transcript_path.exists():
            os.rename(transcript_path, new_transcript_path)
        else:
            print(f"{line_image} transcription does not exist")

def create_line_name_file():
    image_names = ''    
    derge_transcriptions = list(Path('./data/derge_tenjur/transcriptions/').iterdir())
    for transcription in derge_transcriptions:
        transcription_name = transcription.stem
        image_names += transcription_name + '\n'
    Path('./data/derge_images.txt').write_text(image_names)


def update_line_name_in_file():
    new_list = ''
    lithang_images = Path('./data/lithang_kanjur/lithang_images.txt').read_text().split('\n')
    lithang_name_changed = Path('./data/lithang_kanjur/lithang_name_changed.txt/').read_text().split('\n')
    for image in lithang_images:
        if image in lithang_name_changed:
            new_image_name = "LIKA_" + image
            new_list += new_image_name + '\n'
        else:
            new_list += image + '\n'
    Path('./data/updated_lithang_images.txt').write_text(new_list)


if __name__ == '__main__':
    get_same_line_names()