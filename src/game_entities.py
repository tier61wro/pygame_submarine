import logging
from random import randrange

import pygame

from graphic import cargoStand, planeStand


class DrawableObject:
    def __init__(self, x: int, y: int, sprite=None):
        self.x = x
        self.y = y
        self.sprite = sprite

    def draw(self, win):
        if self.sprite:
            win.blit(self.sprite, (self.x, self.y))
        else:
            # Стандартная отрисовка, если спрайт не задан
            pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, 2, 5))


class Submarine(DrawableObject):
    DEFAULT_VELOCITY = 10

    def __init__(self, x: int, y: int, sprite):
        super().__init__(x, y, sprite)
        self.vel = self.DEFAULT_VELOCITY
        self._alive = True

    @property
    def width(self):
        _width = 0
        if self.sprite:
            _width = self.sprite.get_width()
        logging.debug(f'submarine width = {_width}')
        return _width

    @property
    def height(self):
        _height = 0
        if self.sprite:
            _height = self.sprite.get_height()
        logging.debug(f'submarine height = {_height}')
        return _height

    @property
    def rocket_launcher_point(self):
        return self.width - 20

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, val):
        if not isinstance(val, bool):
            raise TypeError("Value must be bool")
        self._alive = val
        if not self._alive:
            logging.info("Submarine was destroyed")


class Torpedo(DrawableObject):
    DEFAULT_VELOCITY = 10

    def __init__(self, x: int, y: int, object_type: str, sprite=None):
        super().__init__(x, y, sprite)
        self.object_type = object_type
        self.vel = self.DEFAULT_VELOCITY
        if self.object_type == 'fast':
            self.vel = self.DEFAULT_VELOCITY * 2


class Bomb(DrawableObject):
    DEFAULT_VELOCITY = 10

    @staticmethod
    def gen_bomb_speed():
        min_speed = 6
        max_speed = 10
        return randrange(min_speed, max_speed + 1)

    def __init__(self, x: int, y: int, object_type=None):
        super().__init__(x, y, sprite=None)
        self.vel = Bomb.gen_bomb_speed()
        self.object_type = object_type
        if self.object_type == 'fast':
            self.vel = self.vel * 2


class Plane:
    min_velocity = 5
    max_velocity = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 100
        self.vel = self.gen_random_velocity()
        self.last_bomb = pygame.time.get_ticks()

    @classmethod
    def gen_random_velocity(cls):
        return randrange(cls.min_velocity, cls.max_velocity)

    def draw(self, win):
        win.blit(planeStand, (self.x, self.y))

    def create_bomb(self, bombs):
        curr_time = pygame.time.get_ticks()
        if (curr_time - self.last_bomb) > 1000:
            self.last_bomb = curr_time
            file = '../music/1_torpeda.mp3'
            pygame.mixer.music.load(file)
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play()
            bombs.append(Bomb(self.x + self.width / 2, self.y + self.height, 'regular'))
        return bombs


class Enemy_Ship(DrawableObject):
    def __init__(self, x, y, object_type='regular'):
        super().__init__(x, y)
        self.object_type = object_type
        self.height = 40
        self.y = self.y - self.height
        self.width = 130
        self.sprite = cargoStand
        self.vel = 10 if object_type == 'fast' else 5

    def draw(self, win):
        logging.debug(f"x = {self.x}, y = {self.y}")
        win.blit(self.sprite, (self.x, self.y))
