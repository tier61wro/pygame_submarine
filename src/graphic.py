import os

import pygame

current_dir = os.path.dirname(os.path.abspath(__file__))
images_folder = os.path.join(current_dir, '..', 'images')
# images_folder = '../images'
planeStand = pygame.image.load(os.path.join(images_folder, 'plane.png'))
cargoStand = pygame.image.load(os.path.join(images_folder, 'cargo.png'))
submarineStand = pygame.image.load(os.path.join(images_folder, 'submarine.png'))
