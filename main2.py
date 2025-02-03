import pygame
import sys
import os
import math

from basic_functions import terminate, load_image, load_level, load_sprites

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
YELLOW = pygame.Color(255, 228, 181)
SIZE = WIDTH, HEIGHT = (500, 500)
FPS = 60


def start_screen():
    intro_text = ["TURNINGLIGHTS", "",
                  "Правила игры", "",
                  "Вам необходимо успеть зажечь все лампочки,",
                  "для этого нажимайте на стрелочки",
                  "(в зависимостиот того, где находится лампочка.",
                  "За сбор монеток вы получите",
                  "секретное сообщение!", "", "Удачи!"]

    fon = pygame.transform.scale(load_image('bg.jpeg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, WHITE)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    end_text = ["Проигрышь!", "Попробуйте ещё раз!"]

    fon = pygame.transform.scale(load_image('bg.jpeg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    # font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in end_text:
        string_rendered = font.render(line, 1, WHITE)
        end_rect = string_rendered.get_rect()
        text_coord += 10
        end_rect.top = text_coord
        end_rect.x = 10
        text_coord += end_rect.height
        screen.blit(string_rendered, end_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def win_screen():
    end_text = ["Поздравляем!!!", "Вы прошли игру!!!", f"Количество секретных монет: {len(coins_grop)}"]

    fon = pygame.transform.scale(load_image('bg.jpeg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    # font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in end_text:
        string_rendered = font.render(line, 1, WHITE)
        end_rect = string_rendered.get_rect()
        text_coord += 10
        end_rect.top = text_coord
        end_rect.x = 10
        text_coord += end_rect.height
        screen.blit(string_rendered, end_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


# отрисовка
def generate_level(level):
    new_player, x, y = None, None, None
    playerx, playery = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Box('wall', x, y)
            elif level[y][x] == '&':
                Tile('empty', x, y)
                Lamp('object', x, y)
            elif level[y][x] == '*':
                Tile('empty', x, y)
                Coin('coin', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                playerx, playery = x, y
    # sprite_sheet = pygame.image.load("rey.png").convert_alpha()

    new_player = Player(playerx, playery)

    return new_player, x, y


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('floor.png'),
    'object': load_image('light-off.png'),
    'object2': load_image('light-on.png'),
    'coin': load_image('coin.png')
}

# player_image = load_image('mar.png')


tile_width = tile_height = 50



class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Box(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(box_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Lamp(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(lamp_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Coin(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(coins_grop, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class CompletedLamp(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(c_lamp_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


sprite_sheet = pygame.image.load("rey.png")

sprite_width = 44
sprite_height = 48
sprites = load_sprites(sprite_sheet, sprite_width, sprite_height)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.images = sprites
        self.index = 1
        self.image = self.images[self.index]
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.x = pos_x
        self.y = pos_y
        # self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update_down(self):
        now = pygame.time.get_ticks()
        self.index = 1
        if now - self.last_update > 10:
            self.index -= self.animation_speed
            if self.index == 0:
                self.image = self.images[int(self.index)]
                self.last_update = now
        if now - self.last_update > 10:
            self.index += self.animation_speed
            if self.index == 1:
                self.image = self.images[int(self.index)]
                self.last_update = now
        if now - self.last_update > 10:
            self.index += self.animation_speed
            if self.index == 2:
                self.image = self.images[int(self.index)]
                self.last_update = now
        if now - self.last_update > 10:
            self.index -= self.animation_speed
            if self.index == 1:
                self.image = self.images[int(self.index)]
                self.last_update = now

    def update_left(self):
        now = pygame.time.get_ticks()
        self.index = 4
        if now - self.last_update > 10:
            self.index -= self.animation_speed
            if self.index == 3:
                self.image = self.images[int(self.index)]
                self.last_update = now
        if now - self.last_update > 10:
            self.index += self.animation_speed
            if self.index == 4:
                self.image = self.images[int(self.index)]
                self.last_update = now
        if now - self.last_update > 10:
            self.index += self.animation_speed
            if self.index == 5:
                self.image = self.images[int(self.index)]
                self.last_update = now
        if now - self.last_update > 10:
            self.index -= self.animation_speed
            if self.index == 4:
                self.image = self.images[int(self.index)]
                self.last_update = now

    def update_right(self):
        now = pygame.time.get_ticks()
        self.index = 7
        if now - self.last_update > 10:
            self.index -= self.animation_speed
            if self.index == 6:
                self.image = self.images[int(self.index)]
                self.last_update = now
        if now - self.last_update > 10:
            self.index += self.animation_speed
            if self.index == 7:
                self.image = self.images[int(self.index)]
                self.last_update = now
        if now - self.last_update > 10:
            self.index += self.animation_speed
            if self.index == 8:
                self.image = self.images[int(self.index)]
                self.last_update = now
        if now - self.last_update > 10:
            self.index -= self.animation_speed
            if self.index == 7:
                self.image = self.images[int(self.index)]
                self.last_update = now

    def update_up(self):
        now = pygame.time.get_ticks()
        self.index = 10
        if now - self.last_update > 10:
            self.index -= self.animation_speed
            if self.index == 9:
                self.image = self.images[int(self.index)]
                self.last_update = now
        if now - self.last_update > 10:
            self.index += self.animation_speed
            if self.index == 10:
                self.image = self.images[int(self.index)]
                self.last_update = now
        if now - self.last_update > 10:
            self.index += self.animation_speed
            if self.index == 11:
                self.image = self.images[int(self.index)]
                self.last_update = now
        if now - self.last_update > 10:
            self.index -= self.animation_speed
            if self.index == 10:
                self.image = self.images[int(self.index)]
                self.last_update = now

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, key):
        delta_x, delta_y = 0, 0
        d_x, d_y = 0, 0
        if key == pygame.K_UP:
            self.update_up()
            delta_x, delta_y = 0, -tile_height
            d_x, d_y = 0, -1
        if key == pygame.K_DOWN:
            self.update_down()
            delta_x, delta_y = 0, tile_height
            d_x, d_y = 0, 1
        if key == pygame.K_LEFT:
            self.update_left()
            delta_x, delta_y = -tile_height, 0
            d_x, d_y = -1, 0
        if key == pygame.K_RIGHT:
            self.update_right()
            delta_x, delta_y = tile_height, 0
            d_x, d_y = 1, 0
        self.rect = self.rect.move(delta_x, delta_y)
        self.pos_x += d_x
        self.pos_y += d_y
        # print(self.pos_x, self.pos_y)
        if pygame.sprite.spritecollideany(self, box_group):
            self.rect = self.rect.move(-delta_x, -delta_y)
            self.pos_x -= d_x
            self.pos_y -= d_y
        if pygame.sprite.spritecollideany(self, lamp_group):
            if pygame.sprite.spritecollideany(self, c_lamp_group):
                self.rect = self.rect.move(-delta_x, -delta_y)
                self.pos_x -= d_x
                self.pos_y -= d_y
            else:
                Tile('empty', self.pos_x, self.pos_y)
                CompletedLamp('object2', self.pos_x, self.pos_y)
                self.rect = self.rect.move(-delta_x, -delta_y)
                self.pos_x -= d_x
                self.pos_y -= d_y


player = None
# camera = Camera()
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("TurningLights")


all_sprites = pygame.sprite.Group()
lamp_group = pygame.sprite.Group()
c_lamp_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
coins_grop = pygame.sprite.Group()
clock = pygame.time.Clock()
mapp = 1
player, level_x, level_y = generate_level(load_level('data/map.txt'))
font = pygame.font.SysFont(None, 35)
timer = 20
arc_timer = 100
text = font.render(str(timer), True, WHITE)

timer_event = pygame.USEREVENT+1
pygame.time.set_timer(timer_event, 1000)


def drawArc(surf, color, center, radius, width, end_angle):
    arc_rect = pygame.Rect(0, 0, radius*2, radius*2)
    arc_rect.center = center
    pygame.draw.arc(surf, color, arc_rect, 0, end_angle, width)


start_screen()

# GAME ----------
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: terminate()
        if event.type == pygame.KEYDOWN: player.move(event.key)
        if event.type == timer_event:
            timer -= 1
            arc_timer -= 5
            text = font.render(str(timer), True, WHITE)
            if timer == 0 and len(c_lamp_group) != len(lamp_group):
                end_screen()
            elif timer == 0:
                mapp += 1
                if mapp != 6:
                    all_sprites = pygame.sprite.Group()
                    lamp_group = pygame.sprite.Group()
                    c_lamp_group = pygame.sprite.Group()
                    box_group = pygame.sprite.Group()
                    player_group = pygame.sprite.Group()
                    coins_grop = pygame.sprite.Group()
                    player, level_x, level_y = generate_level(load_level(f'data/map{mapp}.txt'))
                    timer = 20
                    arc_timer = 100
                    screen.blit(text, (16, 18))
                    drawArc(screen, YELLOW, (32, 32), 32, 5, 2 * math.pi * arc_timer / 100)
                else:
                    win_screen()
    screen.fill(BLACK)
    all_sprites.draw(screen)
    all_sprites.update()
    screen.blit(text, (16, 18))
    drawArc(screen, YELLOW, (32, 32), 32, 5, 2 * math.pi * arc_timer / 100)
    pygame.display.flip()