import pygame

from graphic import cargoStand, planeStand


class DrawableObject:
    def __init__(self, x, y, sprite=None):
        self.x = x
        self.y = y
        self.sprite = sprite

    def draw(self, win):
        if self.sprite:
            win.blit(self.sprite, (self.x, self.y))
        else:
            # Стандартная отрисовка, если спрайт не задан
            pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, 2, 5))


class Torpedo(DrawableObject):
    def __init__(self, x: float, y: float, torpedo_type: str, sprite=None, vel: int = 8):
        super().__init__(x, y, sprite)
        self.torpedo_type = torpedo_type
        self.vel = vel


class Torpedo_old:
    def __init__(self, x, y, torpedo_type):
        self.x = x
        self.y = y
        self.vel = 8
        self.type = torpedo_type

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, 2, 5))


class Bomb:
    def __init__(self, x, y, bomb_type):
        self.x = x
        self.y = y
        self.vel = 10

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, 2, 5))


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
            bombs.append(Bomb(self.x + self.width / 2, self.y + self.height, 'ordinary'))
        return bombs


class Enemy:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.size = 30
        if self.type == 'ordinary':
            self.vel = 5
            self.size = 130
        else:  # fast
            self.vel = 10
            self.size = 130

    def draw(self, win):
        win.blit(cargoStand, (self.x, self.y))
