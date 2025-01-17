import pygame
import sys
import os

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
SIZE = WIDTH, HEIGHT = (500, 500)
FPS = 60


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

# MENU -----------


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


def load_level(filename):
    # filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


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
            elif level[y][x] == '@':
                Tile('empty', x, y)
                playerx, playery = x, y
    new_player = Player(playerx, playery)

    return new_player, x, y


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png'),
    'object': load_image('light-off.png'),
    'object2': load_image('light-on.png')
}

player_image = load_image('mar.png')

tile_width = tile_height = 50


# class Camera:
#     # зададим начальный сдвиг камеры
#     def __init__(self):
#         self.dx = 0
#         self.dy = 0
#
#     # сдвинуть объект obj на смещение камеры
#     def apply(self, obj):
#         obj.rect.x += self.dx
#         obj.rect.y += self.dy
#
#     # позиционировать камеру на объекте target
#     def update(self, target):
#         self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
#         self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


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


class CompletedLamp(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(c_lamp_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.x = pos_x
        self.y = pos_y
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, key):
        delta_x, delta_y = 0, 0
        d_x, d_y = 0, 0
        if key == pygame.K_UP:
            delta_x, delta_y = 0, -tile_height
            d_x, d_y = 0, -1
        if key == pygame.K_DOWN:
            delta_x, delta_y = 0, tile_height
            d_x, d_y = 0, 1
        if key == pygame.K_LEFT:
            delta_x, delta_y = -tile_height, 0
            d_x, d_y = -1, 0
        if key == pygame.K_RIGHT:
            delta_x, delta_y = tile_height, 0
            d_x, d_y = 1, 0
        self.rect = self.rect.move(delta_x, delta_y)
        self.pos_x += d_x
        self.pos_y += d_y
        print(self.pos_x, self.pos_y)
        if pygame.sprite.spritecollideany(self, box_group):
            self.rect = self.rect.move(-delta_x, -delta_y)
            self.pos_x -= d_x
            self.pos_y -= d_y
        if pygame.sprite.spritecollideany(self, lamp_group):
            Tile('empty', self.pos_x, self.pos_y)
            CompletedLamp('object2', self.pos_x, self.pos_y)
            print(self.pos_x, self.pos_y)
            self.rect = self.rect.move(-delta_x, -delta_y)
            self.pos_x -= d_x
            self.pos_y -= d_y


player = None
# camera = Camera()
pygame.init()
screen = pygame.display.set_mode(SIZE)

all_sprites = pygame.sprite.Group()
lamp_group = pygame.sprite.Group()
c_lamp_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
clock = pygame.time.Clock()
player, level_x, level_y = generate_level(load_level('data/map.txt'))

start_screen()
# GAME ----------
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: terminate()
        if event.type == pygame.KEYDOWN:
            player.move(event.key)
    # camera.update(player)
    for sprite in all_sprites:
        pass
        # camera.apply(sprite)
    screen.fill(BLACK)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()

# pygame.quit()
