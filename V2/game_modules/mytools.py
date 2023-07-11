import pygame
from pygame.locals import *
import pygame_gui as pg_gui
import json

def read_json_file(path):
    json_data=None
    with open(path) as json_file:
        json_data = json.load(json_file)

    return json_data

def write_json_file(path, data):
    json_string = json.dumps(data)
    with open(path, 'w') as outfile:
        outfile.write(json_string)