import pytmx
import pygame

import os

import random
from Room.Room import Room

def loadRoom(room_type='basement'):

    room_folder = os.path.join('res/floors/', room_type)
    map_files = [f for f in os.listdir(room_folder) if f.endswith('.tmx')]
    if len(map_files) == 0:
        raise FileNotFoundError(f"'{room_folder}' is empty.")
    
    random_room_file = random.choice(map_files)
    file_name = os.path.join(room_folder, random_room_file)

    tmx_data = pytmx.TiledMap(file_name)

    types = ('obstacle', 'pickup', 'enemy')
    datas = {t : [] for t in types}

    layers = (
        tmx_data.get_layer_by_name('Obstacle Layer'),
        tmx_data.get_layer_by_name('Pickup Layer'),
        tmx_data.get_layer_by_name('Enemy Layer'),
    )
    for layer in layers:
        for x, y, gid in layer:
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

    selected_rooms = []
    end_rooms = []

    while not (len(end_rooms) == 5 and len(selected_rooms) == size):
        selected_rooms = [(0, 0)]
        end_rooms = []

        current_rooms = [(0, 0)]
        next_rooms = []
        while len(current_rooms) != 0:
            for room in current_rooms:
                
                child_flag = False
                x, y = room

                random.shuffle(moves)
                for mx, my in moves:
                    cx, cy = x + mx, y + my
                    n_of_neighbor = sum((cx + mx, cy + my) in selected_rooms for mx, my in moves)
                    if (cx, cy) not in selected_rooms and random.random() < 0.5 and n_of_neighbor == 1 and len(selected_rooms) < size:
                        child_flag = True
                        selected_rooms.append((cx, cy))
                        next_rooms.append((cx, cy))
                
                if child_flag == False:
                    end_rooms.append((x, y))

            current_rooms = next_rooms
            next_rooms = []

    floor = {}
    max_distance = -1
    boss_pos = None
    for pos in end_rooms:
        d = sum(map(abs, pos))
        if max_distance < d:
            max_distance = d
            boss_pos = pos
    floor[boss_pos] = Room("boss", boss_pos, loadRoom())

    for pos in selected_rooms:
        if pos not in floor:
            floor[pos] = Room(room_type, pos, loadRoom())

    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for pos, room in floor.items():
        x, y = pos
        for i, (dx, dy) in enumerate(moves):
            next_pos = (x + dx, y + dy)
            if next_pos in floor:
                door_type = "door" if pos != boss_pos and next_pos != boss_pos else "boss_door"
                room.addDoor(i, door_type)

    return floor

    """ while len(rooms) < size:
        x, y = pos = random.choice(list(neighbor))

        rooms.add(pos)
        for dx, dy in moves:
            neighbor.add((x + dx, y + dy))

    floor = {pos : Room(room_type, pos, loadRoom(room_type)) for pos in rooms}



    return floor """