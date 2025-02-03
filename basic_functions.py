import pygame
import sys
import os
import math


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        # print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    # filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_sprites(sheet, sprite_width, sprite_height):
    sprites = []
    for y in range(0, sheet.get_height(), sprite_height):
        for x in range(0, sheet.get_width(), sprite_width):
            rect = pygame.Rect(x, y, sprite_width, sprite_height)
            image = sheet.subsurface(rect)
            sprites.append(image)
    return sprites