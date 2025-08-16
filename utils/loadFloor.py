import pytmx
import pygame

import os

import random
from Room.Room import Room

def loadRoom(room_type='basement'):

    room_folder = os.path.join('assets/maps/', room_type)
    map_files = [f for f in os.listdir(room_folder) if f.endswith('.tmx')]
    if len(map_files) == 0:
        raise FileNotFoundError(f"'{room_folder}' is empty.")
    
    random_room_file = random.choice(map_files)
    file_name = os.path.join(room_folder, random_room_file)

    tmx_data = pytmx.TiledMap(file_name)

    types = ('obstacle', 'pickup', 'enemy')
    datas = {t : [] for t in types}

    data_layer = tmx_data.get_layer_by_name('Tile Layer 1')
    for x, y, gid in data_layer:
        if not gid:
            continue

        properties = tmx_data.get_tile_properties_by_gid(gid)

        tile_type = properties.get('type')
        tile_name = properties.get('name')
        try:
            datas[tile_type].append((tile_name, x, y))
        except:
            pass

    return datas

def loadFloor(room_type='basement', size=10):

    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    rooms = set()
    neighbor = set([(0, 0)])

    while len(rooms) < size:
        x, y = pos = random.choice(list(neighbor))

        rooms.add(pos)
        for dx, dy in moves:
            neighbor.add((x + dx, y + dy))

    floor = {pos : Room(room_type, pos, loadRoom(room_type)) for pos in rooms}

    for (x, y), room in floor.items():
        for i, (dx, dy) in enumerate(moves):
            if (x + dx, y + dy) in floor:
                room.addDoor(i, room.variant)

    return floor