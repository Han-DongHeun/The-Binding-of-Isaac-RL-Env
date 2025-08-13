import pytmx
import pygame

import os

import random

def loadFloor(room_type='basement'):

    room_folder = os.path.join('assets/maps/', room_type)
    map_files = [f for f in os.listdir(room_folder) if f.endswith('.tmx')]
    if len(map_files) == 0:
        raise FileNotFoundError(f"'{room_folder}' is empty.")
    
    random_room_file = random.choice(map_files)
    file_name = os.path.join(room_folder, random_room_file)


    tmx_data = pytmx.load_pygame(file_name, pixelalpha=True)

    types = ('obstacle', 'pickup', 'enemy')
    datas = dict.fromkeys(types, [])

    data_layer = tmx_data.get_layer_by_name('Data')
    for x, y, gid in data_layer:
        if gid == 0:
            continue

        properties = tmx_data.get_tile_properties_by_gid(gid)

        tile_type = properties.get('type')
        tile_name = properties.get('name')

        datas[tile_type].append((tile_name, x, y))

    return datas