"""
file: configs.py
author: Cytrogen
"""
import json
import pygame


SCREEN_SIZE = (600, 400)
CENTER_SIZE = (300, 200)
TITLE_SIZE = (300, 100)
SUBTITLE_SIZE = (300, 150)
FONT = 'font/Fusion Pixel.ttf'


COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 128, 0),
    'dark_grey': (84, 84, 84),
    'light_grey': (172, 172, 172),
    'yellow': (255, 255, 0)
}


pygame.init()
surface = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Doggo Fight')


def manipulate_json_file(action: str, data: dict | None, is_user: bool = True) -> dict | None:
    """
    Manipulate the JSON file. If is_user is True, then manipulate dog.json,
    otherwise manipulate enemy.json.
    操作JSON文件。如果is_user为True，则操作dog.json，否则操作enemy.json。
    :param action:
    :param data:
    :param is_user:
    :return:
    """
    if is_user:
        file_name = 'data/dog.json'
    else:
        file_name = 'data/enemy.json'

    with open(file_name, 'r', encoding='UTF-8') as json_file:
        json_data = json.load(json_file)

        match action:
            case 'add':
                json_data.update(data)

            case 'modify':
                for key, value in data.items():
                    json_data[key] = value

            case 'read':
                return json_data

    with open(file_name, 'w', encoding='UTF-8') as json_file:
        json.dump(json_data, json_file, indent=4)
    return None
