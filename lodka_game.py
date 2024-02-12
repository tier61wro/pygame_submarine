import logging
import os
import time
from typing import List

import pygame

from graphic import cargoStand, lodkaStand
from ships_and_enemies_classes import Plane, Torpedo

clock = pygame.time.Clock()

# background music
pygame.mixer.init()
pygame.mixer.music.load("music/sonar.mp3.mpg")
# pygame.mixer.music.load("music/sonar2.mp3.mpg")
# pygame.mixer.music.load("music/expl.mp3.mpg")

pygame.mixer.music.play(1000, 0)

# логгирование
logging.basicConfig(filename='logfile.log', level=logging.INFO)
logging.info('GAME STARTED')

# подгружаем изображения
images_folder = './images'

pygame.init()
run = True
win_width = 1000
win_height = 500
win = pygame.display.set_mode((win_width, win_height))
bg = pygame.image.load(os.path.join(images_folder, 'bg.png'))

pygame.display.set_caption("submarine game")
myfont = pygame.font.SysFont("monospace", 16)

clock = pygame.time.Clock()

# submarine params
lodka_x = 50
lodka_y = 425
lodka_width = 130
lodka_height = 39
lodka_speed = 10
lodka_alive = 1
double_speed = lodka_speed * 2

torpedos: List = []
enemies: List = []
planes: List = []
bombs: List = []
score = 0


class Enemy():
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


def drawWindow():
    global bombs
    for torpeda in torpedos:
        torpeda.draw(win)

    for enemy in enemies:
        enemy.draw(win)

    for plane in planes:
        bombs = plane.create_bomb(bombs)
        plane.draw(win)

    for bomb in bombs:
        bomb.draw(win)

    pygame.display.update()


def drawBg():
    win.blit(bg, (0, 0))


# MAIN LOOP START
while run:
    clock.tick(10)  # better then : pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    disclaimer_text = myfont.render("Round 1", 1, (0, 0, 0))
    gameover_text = myfont.render("GAME OVER", 1, (0, 0, 0))
    score_text = myfont.render("Score {0}".format(score), 1, (0, 0, 0))
    reload_text = myfont.render("Reloading in {0}".format('3'), 1, (0, 0, 0))
    currentColor = (255, 255, 255)

    if lodka_alive == 0:
        win.fill(currentColor)
        win.blit(gameover_text, (5, 480))
        pygame.display.update()
        time.sleep(3)
        run = False
        break

    else:
        drawBg()
        win.blit(disclaimer_text, (5, 480))
        win.blit(score_text, (5, 10))
        win.blit(reload_text, (win_width - 150, win_height - 20))
        win.blit(lodkaStand, (lodka_x, lodka_y))

        for torpedo in torpedos:
            for enemy in enemies:
                if (torpedo.y < 95) and ((torpedo.x > enemy.x) and (torpedo.x < enemy.x + enemy.size)):
                    logging.info('enemy was killed')
                    score += 1
                    enemies.pop(enemies.index(enemy))

            if torpedo.y < win_height and torpedo.y > 95:
                torpedo.y -= 10
            else:
                torpedos.pop(torpedos.index(torpedo))

        for bomb in bombs:
            logging.debug("bombx = {}, bomby = {}".format(bomb.lodka_x, bomb.lodka_y))
            logging.debug("x = {}, y = {}".format(lodka_x, lodka_y))
            if (bomb.lodka_x < lodka_x + lodka_width) \
                    and (bomb.lodka_x > lodka_x) \
                    and (bomb.lodka_y > lodka_y) \
                    and (bomb.lodka_y < lodka_y + lodka_height):

                logging.info('submarine was killed')
                # pygame.mixer.music.load("music/expl.mp3")
                # pygame.mixer.music.play(1, 0)
                lodka_alive = 0
                win.fill(currentColor)
                break
            elif bomb.lodka_y > win_height:
                logging.info('bomb was popped')
                bombs.pop(bombs.index(bomb))

        for enemy in enemies:
            if enemy.x < win_width and enemy.y > 0:
                # logging.info("we moved enemy")
                enemy.x += enemy.vel
            else:
                enemies.pop(enemies.index(enemy))

        for plane in planes:
            if plane.x < win_width and plane.y > 0:
                plane.x -= plane.vel
                cur_time = pygame.time.get_ticks()
                # logging.info("current time  = " + str(cur_time))
            else:
                enemies.pop(planes.index(plane))

        for bomb in bombs:
            if bomb.lodka_y < win_height:
                bomb.lodka_y += bomb.vel
                # logging.info("we moved bomb")
            else:
                bombs.pop(bombs.index(bomb))

        # pygame.display.update()
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and lodka_x > 0:
            lodka_x -= lodka_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and lodka_x < win_width - lodka_width - 5:
            lodka_x += lodka_speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and lodka_y > 5:
            lodka_y -= lodka_speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and lodka_y < win_height - lodka_height - 5:
            lodka_y += lodka_speed
        if keys[pygame.K_SPACE]:
            # launch torpedo
            torpedos.append(
                Torpedo(
                    round(lodka_x + lodka_width // 2),
                    round(lodka_y + lodka_height // 2),
                    'ordinary'
                )
            )
        if keys[pygame.K_o]:
            # create Enemy
            # logging.info("we added enemy to list")
            enemies.append(Enemy(20, 87, 'ordinary'))
        if keys[pygame.K_f]:
            # create Enemy
            # logging.info("we added enemy to list")
            enemies.append(Enemy(20, 87, 'fast'))
        if keys[pygame.K_p]:
            # create Plane
            logging.info("we added plane to list")
            planes.append(Plane(win_width - 10, 10))

        drawWindow()

pygame.quit()
