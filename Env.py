from utils.func import *
from Character.Character import *
from Room.Room import *
from Pickup.Bomb import *
from Pickup.TrollBomb import *

import numpy as np

import pygame

from utils.const import *
from utils.loadFloor import loadFloor

class IsaacEnv:
    posMoves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, play_mode=HUMAN_MODE):
        self.play_mode = play_mode
        self.screen = pygame.Surface((WIDTH, HEIGHT))

        self.floor = loadFloor("basement")
        self.floor_key = "basement"
        self.floor_idx = 0
        self.currentRoom = (0,0)
        self.animatingRooms: list[Room] = []

        self.minimap = pygame.Surface((textures["map"]["background"].get_width(), textures["map"]["background"].get_height())).convert_alpha()
        self.minimap.set_clip()
        self.minimap_rect = self.minimap.get_rect(topright=(WIDTH - GRIDX + GRATIO, GRIDY - GRATIO))

        self.updateFloor()
        self.updateMinimap()

        self.controls = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.isaac = Character(self.controls)

    def updateMinimap(self):
        # Draw the minimap
        if not self.play_mode:
            return

        self.minimap.fill((0,0,0,0))
        self.minimap.blit(textures["map"]["background"], (0, 0))
        for room in self.floor:
            self.floor[room].renderMap(self.minimap, self.currentRoom, False)
        for room in self.floor:
            self.floor[room].renderMap(self.minimap, self.currentRoom, True)

    def updateFloor(self):
        # Check if you've been in a room

        self.floor[self.currentRoom].entered = True

        for m in self.posMoves:
            mx, my = m
            x, y = self.currentRoom
            newPos = (mx + x, my + y)

            if newPos in self.floor:
                self.floor[newPos].seen = True

    def moveNextRoom(self, move):
        next_x = move[0] + self.currentRoom[0]
        next_y = move[1] + self.currentRoom[1]
        nextRoom = (next_x, next_y)

        if nextRoom == self.currentRoom or nextRoom not in self.floor:
            return

        old = self.currentRoom
        self.currentRoom = (next_x, next_y)

        # Animate the room
        self.floor[self.currentRoom].animateIn(move)
        self.floor[old].animateOut(move)

        # Animate the room
        self.animatingRooms.append(self.floor[self.currentRoom])
        self.animatingRooms.append(self.floor[old])

        # Animate isaac with the room
        gx = 6 - 6 * move[0]
        gy = 3 - 3 * move[1]
        self.isaac.x, self.isaac.y = get_center(gx, gy)

        # Remove tears from an animating room
        self.isaac.clearTears()

        self.floor[self.currentRoom].entered = True

        for mx, my in self.posMoves:
            x, y = self.currentRoom
            newPos = (mx + x, my + y)

            if newPos in self.floor:
                self.floor[newPos].seen = True

        self.updateMinimap()

    def step(self, actions: np.ndarray):

        actions = actions.tolist()
        self.isaac.moving(dict(enumerate(actions[:8])))
        if actions[8] and self.isaac.pickups[1].use(1):
            self.floor[self.currentRoom].other.append(TrollBomb(self.floor[self.currentRoom], 0, get_grid_coord(self.isaac.x, self.isaac.y), self.isaac))

        # Draw animating rooms (The ones that are shifting in and out of frame)
        if len(self.animatingRooms) > 0:
            for r in self.animatingRooms:
                r.render(self.screen, self.isaac)
            self.animatingRooms = [r for r in self.animatingRooms if r.animating]
        else:
            self.screen.fill((0,0,0))

            # Render the room
            move = self.floor[self.currentRoom].render(self.screen, self.isaac)
            self.moveNextRoom(move)

        # DRAW MAP
        if self.play_mode:
            self.screen.blit(self.minimap, self.minimap_rect)

        n_of_bombs = self.isaac.pickups[1].score

        observations = pygame.surfarray.array3d(self.screen)
        terminated = self.isaac.dead

        return (observations, terminated)