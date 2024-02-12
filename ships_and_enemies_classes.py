import pygame

from graphic import planeStand


class Torpedo:
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
            file = 'music/1_torpeda.mp3'
            pygame.mixer.music.load(file)
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play()
            bombs.append(Bomb(self.x + self.width / 2, self.y + self.height, 'ordinary'))
        return bombs
