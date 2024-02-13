import logging

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
    def __init__(self, x: int, y: int, sprite):
        super().__init__(x, y, sprite)
        self.vel = 10
        self.width = 130
        self.height = 39
        self.alive = True


class Torpedo(DrawableObject):
    def __init__(self, x: int, y: int, object_type: str, sprite=None):
        super().__init__(x, y, sprite)
        self.object_type = object_type
        self.vel = 8
        if self.object_type == 'fast':
            self.vel = 16


class Bomb(DrawableObject):
    def __init__(self, x: int, y: int, object_type=None):
        super().__init__(x, y, sprite=None)
        self.vel = 10
        self.object_type = object_type
        if self.object_type == 'fast':
            self.vel = 20


class Plane:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 100
        self.vel = 8  # TODO make it random (5 - 10)
        self.last_bomb = pygame.time.get_ticks()

    def draw(self, win):
        # pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.size, 8))
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
        self.vel = 5
        if object_type == 'fast':  # fast
            self.vel = 10

    def draw(self, win):
        logging.debug(f"x = {self.x}, y = {self.y}")
        win.blit(cargoStand, (self.x, self.y))
