from pathlib import Path
from my_util import getId

# Считывает фигуры из файлов и возвращает
# список из их элементов
def parse_dir(dir_path):
    pictures_files = []
    for filename in dir_path.iterdir():
        if filename.is_file():
            pictures_files.append(filename)
                
    pictures = []
    for path in pictures_files:
        picture = parse_picture(path)
        pictures.append(picture)
    return pictures


# Считывает файл с фигурой и преобразует
# в список
def parse_picture(path):
    with open(path) as file:
        picture = []
        for line in file:
            line = line.replace('\n', '')
            for char in line:
                picture.append(getId(char))

        return picture

