import logging
import os
import time
from typing import List

import pygame

from game_entities import Enemy_Ship, Plane, Torpedo
from graphic import lodkaStand

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
clock = pygame.time.Clock()

# background music
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(project_root, "music/sonar.mp3.mpg"))


pygame.mixer.music.play(1000, 0)

# логирование
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_file_path = os.path.join(project_root, 'logfile.log')

logging.basicConfig(filename=log_file_path, level=logging.DEBUG)
logging.info('GAME STARTED')

# подгружаем изображения
images_folder = '../images'


pygame.init()
run = True
win_width = 1000
win_height = 500
win = pygame.display.set_mode((win_width, win_height))
bg = pygame.image.load(os.path.join(images_folder, 'bg.png'))

pygame.display.set_caption("submarine game")
myfont = pygame.font.SysFont("monospace", 16)

clock = pygame.time.Clock()
BLACK = (0, 0, 0)

# submarine params
lodka_x = 50
lodka_y = 425
lodka_width = 130
lodka_height = 39
lodka_speed = 10
submarine_alive = True

horizont_level = 165

torpedos: List = []
enemies: List = []
planes: List = []
bombs: List = []
score = 0


def draw_window():
    global bombs
    for torpedo in torpedos:
        torpedo.draw(win)

    for enemy in enemies:
        enemy.draw(win)

    for plane in planes:
        bombs = plane.create_bomb(bombs)
        plane.draw(win)

    for bomb in bombs:
        bomb.draw(win)

    pygame.display.update()


def draw_bg():
    win.blit(bg, (0, 0))


# MAIN GAME LOOP
while run:
    clock.tick(10)  # better then : pygame.time.delay(100)
    for event in pygame.event.get():
        # отвечает за нажатие на крестик в меню, не за ESC
        if event.type == pygame.QUIT:
            run = False

    disclaimer_text = myfont.render("Round 1", 1, (0, 0, 0))
    game_over_text = myfont.render("GAME OVER", 1, (0, 0, 0))
    score_text = myfont.render("Score {0}".format(score), 1, (0, 0, 0))
    reload_text = myfont.render("Reloading in {0}".format('3'), 1, (0, 0, 0))
    currentColor = (255, 255, 255)

    if submarine_alive:
        # The game continues.
        draw_bg()
        win.blit(disclaimer_text, (5, 480))
        win.blit(score_text, (5, 10))
        win.blit(reload_text, (win_width - 150, win_height - 20))
        win.blit(lodkaStand, (lodka_x, lodka_y))
        pygame.draw.line(win, BLACK, (0, horizont_level), (win_width, horizont_level), 1)

        for torpedo in torpedos:
            for enemy in enemies:
                if torpedo.y < horizont_level and enemy.x < torpedo.x < enemy.x + enemy.width:
                    logging.info('enemy was killed')
                    score += 1
                    enemies.pop(enemies.index(enemy))

            if horizont_level < torpedo.y < win_height:
                torpedo.y -= 10
            else:
                torpedos.pop(torpedos.index(torpedo))

        for bomb in bombs:
            logging.debug("bombx = {}, bomby = {}".format(lodka_x, lodka_y))
            logging.debug("x = {}, y = {}".format(lodka_x, lodka_y))
            if lodka_x < bomb.x < lodka_x + lodka_width and lodka_y < bomb.y < lodka_y + lodka_height:
                logging.info('submarine was killed')
                # pygame.mixer.music.load("music/expl.mp3")
                # pygame.mixer.music.play(1, 0)
                submarine_alive = False
                win.fill(currentColor)
                break
            elif bomb.y > win_height:
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
            if bomb.y < win_height:
                bomb.y += bomb.vel
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
                    x=round(lodka_x + lodka_width // 2),
                    y=round(lodka_y + lodka_height // 2),
                    object_type='regular'
                )
            )
        if keys[pygame.K_o]:
            # create a regular Enemy
            # logging.info("we added enemy to list")
            enemies.append(Enemy_Ship(20, horizont_level, 'regular'))
        if keys[pygame.K_f]:
            # create a fast Enemy
            # logging.info("we added enemy to list")
            enemies.append(Enemy_Ship(20, horizont_level, 'fast'))
        if keys[pygame.K_p]:
            # create a Plane
            logging.info("we added plane to list")
            planes.append(Plane(win_width - 10, 10))

        draw_window()

    else:
        # GAME OVER BLOCK
        win.fill(currentColor)
        win.blit(game_over_text, (5, 480))
        pygame.display.update()
        time.sleep(3)
        run = False
        break

pygame.quit()
