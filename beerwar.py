# coding: utf-8

import pygame
import pprint
import os
import requests
from pygame.locals import *
from sys import exit, argv
from pygame import sprite


class BeerWarInterface(object):

    def get_matrix(self):
        response = requests.get("http://localhost:8080/matrix/")
        return response.json()

    def read_matrix(self, matrix):
        # matrix = [['_'] * 10] * 10
        # matrix[4][2]  = "#"
        # matrix[6][2]  = "#"
        pprint.pprint(matrix)

        tank_positions = []
        barriers_positions = []
        for line_index, line in enumerate(matrix):
            for collunm_index, collunm in enumerate(line):
                if collunm == '#':
                    barriers_positions.append(
                        (collunm_index * 50, line_index * 50))
                elif collunm != '_' and collunm != "#":
                    tank_positions.append((collunm_index * 50, line_index * 50))

        return tank_positions, barriers_positions

class GameObjects(sprite.Sprite):

    _base_image_path = 'sprites'

    def __init__(self, position_tuple, image_name, *groups):
        sprite.Sprite.__init__(self, *groups)
        self.position_x, self.position_y = position_tuple
        self.image = pygame.image.load(os.path.sep.join(
                [GameObjects._base_image_path, image_name]))
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.position_x, self.position_y)
        self.degrees = 0
        self.convert_image()

    def rotate(self, side):
        sides = {
            "LEFT": 90,
            "RIGHT": 270
        }

        degrees_to_rotate = sides[side]
        self.set_canon_position()
        self.image = pygame.transform.rotate(self.image, degrees_to_rotate)
        self.convert_image()

    def set_canon_position(self):
        pass

    def get_canon_position(self):
        positions = {
            90: "LEFT",
            180: "DOWN",
            270: "RIGHT",
            0: "UP"
        }

        return positions[self.degrees]

    def move(self, side):
        self.convert_image()
        sides = {
            "LEFT": (-10, 0),
            "RIGHT": (10, 0),
            "UP": (0, -10),
            "DOWN": (0, 10)
        }
        self.rect.move_ip(sides[side])

    def convert_image(self):
        self.image.set_alpha(None, RLEACCEL)
        self.image.convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)

class Game(object):

    FPS = 16
    SCREEN_SIZE = (640, 460)
    NAME = "Beer War"

    keys = {
        K_a: False,
        K_d: False,
        K_LEFT: False,
        K_RIGHT: False,
        K_UP: False,
        K_DOWN: False,
        K_RETURN: False,
        27: False
    }

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(Game.NAME)
        self.screen = pygame.display.set_mode(Game.SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.group = sprite.RenderUpdates()
        self.background = pygame.image.load(os.path.sep.join(
                ["sprites", "background.jpg"])).convert()
        self.screen.blit(self.background, (0, 0))
        self.tanks = []
        self.barriers = []

        # interface with a server
        self.interface = None

    def run(self):
        pygame.display.flip()
        while True:
            self.clock.tick(Game.FPS)

            for e in pygame.event.get([KEYUP, KEYDOWN]):
                valor = (e.type == KEYDOWN)
                if e.key in Game.keys:
                    Game.keys[e.key] = valor

            if self.interface is None:
                if Game.keys[K_LEFT]:
                    self.tanks[0].move("LEFT")
                elif Game.keys[K_RIGHT]:
                    self.tanks[0].move("RIGHT")
                elif Game.keys[K_DOWN]:
                    self.tanks[0].move("DOWN")
                elif Game.keys[K_UP]:
                    self.tanks[0].move("UP")
                elif Game.keys[K_a]:
                    self.tanks[0].rotate("LEFT")
                elif Game.keys[K_d]:
                    self.tanks[0].rotate("RIGHT")
            else:
                matrix = self.interface.get_matrix()
                tanks, barriers = self.interface.read_matrix(matrix)
                for tank in tanks:
                    game.tanks.append(GameObjects(tank, "tanque.png", game.group))
                for barrier in barriers:
                    game.barriers.append(GameObjects(tank, "barrier.png", game.group))


            self.group.clear(self.screen, self.background)
            pygame.display.update(self.group.draw(self.screen))

if __name__ == '__main__':
    game = Game()
    game.tanks.append(GameObjects((0, 0), "tanque.png", game.group))
    #game.interface = BeerWarInterface()
    game.run()
