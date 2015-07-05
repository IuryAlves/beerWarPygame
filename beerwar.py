# coding: utf-8

from pygame.locals import *
from sys import exit, argv
import pygame
import pprint
import os
from pygame import sprite


class BeerWarInterface(object):

    def read_matrix(self):
        matrix = [['_'] * 10 for i in range(10)]
        matrix[4][2]  = "#"
        matrix[6][2]  = "#"
        pprint.pprint(matrix)

        positions = []
        for line_index, line in enumerate(matrix):
            for collunm_index, collunm in enumerate(line):
                if collunm == '#':
                    positions.append((collunm_index * 50, line_index * 50))

        return positions

class Objects(sprite.Sprite):

    _base_image_path = 'sprites'

    def __init__(self, position_tuple, image_name, *groups):
        sprite.Sprite.__init__(self, *groups)
        self.position_x, self.position_y = position_tuple
        self.image = pygame.image.load(os.path.sep.join([Objects._base_image_path, image_name]))
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.position_x, self.position_y)
        self.convert_image()

    def move(self, side):
        self.convert_image()
        if side == 'LEFT':
            x, y = -10, 0
        if side == 'RIGHT':
            x, y = 10, 0
        if side == 'UP':
            x, y = 0, -10
        if side == 'DOWN':
            x, y = 0, 10
        self.rect.move_ip(x, y)

    def convert_image(self):
        self.image.set_alpha(None, RLEACCEL)
        self.image.convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)

class Game(object):

    FPS = 16
    SCREEN_SIZE = (640, 460)
    NAME = "Beer War"

    keys = {
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

    def run(self):
        pygame.display.flip()
        while True:
            self.clock.tick(Game.FPS)

            for e in pygame.event.get([KEYUP, KEYDOWN]):
                valor = (e.type == KEYDOWN)
                if e.key in Game.keys:
                    Game.keys[e.key] = valor

            if Game.keys[K_LEFT]:
                tank.move("LEFT")
            elif Game.keys[K_RIGHT]:
                tank.move("RIGHT")
            elif Game.keys[K_DOWN]:
                tank.move("DOWN")
            elif Game.keys[K_UP]:
                tank.move("UP")

            self.group.clear(self.screen, self.background)
            pygame.display.update(self.group.draw(self.screen))

if __name__ == '__main__':
    game = Game()

    beerwar_interface = BeerWarInterface()
    positions = beerwar_interface.read_matrix()
    for position in positions:
        game.tanks.append(Objects(position, "tanque.png", game.group))

    game.run()
