sprite_sheet = pygame.image.load("rey.png").convert_alpha()


def load_sprites(sheet, sprite_width, sprite_height):
    sprites = []
    for y in range(0, sheet.get_height(), sprite_height):
        for x in range(0, sheet.get_width(), sprite_width):
            rect = pygame.Rect(x, y, sprite_width, sprite_height)
            image = sheet.subsurface(rect)
            sprites.append(image)
    return sprites


sprite_width = 44
sprite_height = 48
sprites = load_sprites(sprite_sheet, sprite_width, sprite_height)


class Player:
    def __init__(self):
        self.images = sprites
        self.index = 1
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.animation_speed = 0.25
        self.last_update = pygame.time.get_ticks()

    def update_down(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.index -= self.animation_speed
            if self.index == 0:
                self.image = self.images[int(self.index)]
                self.last_update = now
            self.index += self.animation_speed
            if self.index == 1:
                self.image = self.images[int(self.index)]
                self.last_update = now
            self.index += self.animation_speed
            if self.index == 2:
                self.image = self.images[int(self.index)]
                self.last_update = now
            self.index -= self.animation_speed
            if self.index == 1:
                self.image = self.images[int(self.index)]
                self.last_update = now

    def update_left(self):
        now = pygame.time.get_ticks()
        self.index = 4
        if now - self.last_update > 100:
            self.index -= self.animation_speed
            if self.index == 3:
                self.image = self.images[int(self.index)]
                self.last_update = now
            self.index += self.animation_speed
            if self.index == 4:
                self.image = self.images[int(self.index)]
                self.last_update = now
            self.index += self.animation_speed
            if self.index == 5:
                self.image = self.images[int(self.index)]
                self.last_update = now
            self.index -= self.animation_speed
            if self.index == 4:
                self.image = self.images[int(self.index)]
                self.last_update = now

    def update_right(self):
        now = pygame.time.get_ticks()
        self.index = 7
        if now - self.last_update > 100:
            self.index -= self.animation_speed
            if self.index == 6:
                self.image = self.images[int(self.index)]
                self.last_update = now
            self.index += self.animation_speed
            if self.index == 7:
                self.image = self.images[int(self.index)]
                self.last_update = now
            self.index += self.animation_speed
            if self.index == 8:
                self.image = self.images[int(self.index)]
                self.last_update = now
            self.index -= self.animation_speed
            if self.index == 7:
                self.image = self.images[int(self.index)]
                self.last_update = now

    def update_up(self):
        now = pygame.time.get_ticks()
        self.index = 10
        if now - self.last_update > 100:
            self.index -= self.animation_speed
            if self.index == 9:
                self.image = self.images[int(self.index)]
                self.last_update = now
            self.index += self.animation_speed
            if self.index == 10:
                self.image = self.images[int(self.index)]
                self.last_update = now
            self.index += self.animation_speed
            if self.index == 11:
                self.image = self.images[int(self.index)]
                self.last_update = now
            self.index -= self.animation_speed
            if self.index == 10:
                self.image = self.images[int(self.index)]
                self.last_update = now

    def draw(self, surface):
        surface.blit(self.image, self.rect)


player = Player()
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= 5
        player.update()  # Обновляем анимацию при движении
    elif keys[pygame.K_RIGHT]:
        player.rect.x += 5
        player.update()  # Обновляем анимацию при движении
    else:
        player.index = 0  # Сброс анимации при остановке

    screen.fill((0, 0, 0))  # Очистка экрана
    player.draw(screen)  # Рисуем игрока
    pygame.display.flip()  # Обновляем экран

    clock.tick(60)  # Ограничение FPS до 60