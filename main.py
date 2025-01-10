import pygame

WHITE = pygame.Color("#ffffff")
BLACK = pygame.Color("#000000")
RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)
SIZE = WIDTH, HEIGHT = (600, 600)


class TurningLights:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        pygame.display.set_caption("TurningLights")

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                cell_x = self.left + self.cell_size * x
                cell_y = self.top + self.cell_size * y
                rect = (cell_x, cell_y, self.cell_size, self.cell_size)
                if self.board[y][x] == -2:
                    pygame.draw.rect(screen, BLUE, rect)
                    pygame.draw.rect(screen, WHITE, rect, 1)
                else:
                    if self.board[y][x] == 0:
                        pygame.draw.rect(screen, WHITE, rect, 1)
                    if self.board[y][x] == -1:
                        pygame.draw.rect(screen, RED, rect)
                        pygame.draw.rect(screen, WHITE, rect, 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)
        else:
            pass

    def get_cell(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        x = (mouse_x - self.left) // self.cell_size
        y = (mouse_y - self.top) // self.cell_size
        if not (0 <= x < self.width and 0 <= y < self.height):
            return None
        else:
            return x, y

    def on_click(self, cell):
        cell_x, cell_y = cell
        if self.board[cell_y][cell_x] == -2:
            self.board[cell_y][cell_x] = 0
        else:
            self.board[cell_y][cell_x] = self.board[cell_y][cell_x] - 1


pygame.init()
screen = pygame.display.set_mode(SIZE)

run = True

board = TurningLights(12, 12)
board.set_view(0, 0, 50)
while run:
    screen.fill(BLACK)
    for event in pygame.event.get():
        run = event.type != pygame.QUIT
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    board.render(screen)
    pygame.display.update()

pygame.quit()
