# import library
import pygame 
import random
import time

# Dimensi layar
WIDTH = 1000
HEIGHT = 600

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Ukuran blok labirin
BLOCK_SIZE = 20

# Inisialisasi Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PAA")

clock = pygame.time.Clock()

# kelas untuk membuat peta
class Maze: 
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[1] * cols for _ in range(rows)]
        self.generate_maze()

    def generate_maze(self):
        stack = [(0, 0)]

        while stack:
            current_cell = stack[-1]

            x, y = current_cell
            self.grid[y][x] = 0

            neighbors = self.get_unvisited_neighbors(x, y)
            if neighbors:
                next_cell = random.choice(neighbors)
                nx, ny = next_cell

                if nx > x:
                    self.grid[y][x + 1] = 0
                elif nx < x:
                    self.grid[y][x - 1] = 0
                elif ny > y:
                    self.grid[y + 1][x] = 0
                elif ny < y:
                    self.grid[y - 1][x] = 0

                stack.append(next_cell)
            else:
                stack.pop()

    def get_unvisited_neighbors(self, x, y):
        neighbors = []
        if x > 1 and self.grid[y][x - 2] == 1:
            neighbors.append((x - 2, y))
        if x < self.cols - 2 and self.grid[y][x + 2] == 1:
            neighbors.append((x + 2, y))
        if y > 1 and self.grid[y - 2][x] == 1:
            neighbors.append((x, y - 2))
        if y < self.rows - 2 and self.grid[y + 2][x] == 1:
            neighbors.append((x, y + 2))
        return neighbors

    def shuffle_map(self):
        self.grid = [[1] * self.cols for _ in range(self.rows)]
        self.generate_maze()

    def draw(self):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x] == 1:
                    pygame.draw.rect(screen, BLACK, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

maze = Maze(30, 40)

# kelas untuk bola
class Ball:
    def __init__(self, color, chase_color):
        self.x = 1
        self.y = 1
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.is_paused = True
        self.color = color
        self.chase_color = chase_color

# menggerakkan droid 
    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < maze.cols and 0 <= new_y < maze.rows and maze.grid[new_y][new_x] == 0:
            self.x = new_x
            self.y = new_y

    def auto_move(self):
        if self.is_paused:
            return

        dx, dy = self.direction
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < maze.cols and 0 <= new_y < maze.rows and maze.grid[new_y][new_x] == 0:
            self.x = new_x
            self.y = new_y
        else:
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x * BLOCK_SIZE + BLOCK_SIZE // 2, self.y * BLOCK_SIZE + BLOCK_SIZE // 2), BLOCK_SIZE // 2)

# kelas untuk menambah tombol
class AddButton:
    def __init__(self, rect, color, text):
        self.rect = rect
        self.color = color
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 20)
        text_render = font.render(self.text, True, WHITE)
        screen.blit(text_render, (self.rect.x + 10, self.rect.y + 10))

    def handle_click(self):
        red_balls.append(Ball(RED, GREEN))
        red_balls[-1].x = random.randint(1, maze.cols - 2)
        red_balls[-1].y = random.randint(1, maze.rows - 2)

#kelas untuk menambah tombol hapus droid
class RemoveButton:
    def __init__(self, rect, color, text):
        self.rect = rect
        self.color = color
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 20)
        text_render = font.render(self.text, True, WHITE)
        screen.blit(text_render, (self.rect.x + 10, self.rect.y + 10))

    def handle_click(self):
        if len(red_balls) > 1:
            red_balls.pop()

# inisialisasi objek map/maze/peta, droid merah & hijau (Membuat objek labirin dengan ukuran 30 baris dan 40 kolom.
# Membuat objek bola merah dengan warna merah dan bola hijau dengan warna hijau.)
red_balls = [Ball(RED, GREEN)] 
green_ball = Ball(GREEN, RED)

# untuk menambahkan tombol tombol
add_button = AddButton(pygame.Rect(835, 320, 130, 40), RED, "TAMBAH MERAH")
remove_button = RemoveButton(pygame.Rect(835, 370, 130, 40), RED, "HAPUS MERAH")

# untuk menambah tombol tombol kontrol (Membuat objek-objek persegi panjang yang mewakili tombol-tombol kontrol pada layar.)
start_button_rect = pygame.Rect(835, 20, 130, 40)
pause_button_rect = pygame.Rect(835, 70, 130, 40)
shuffle_red_button_rect = pygame.Rect(835, 120, 130, 40)
shuffle_green_button_rect = pygame.Rect(835, 170, 130, 40)
shuffle_map_button_rect = pygame.Rect(835, 220, 130, 40)
red_view_button_rect = pygame.Rect(835, 270, 130, 40)

show_red_view = False

# Perubahan posisi awal droid merah dan hijau
red_position = (random.randint(1, maze.cols - 2), random.randint(1, maze.rows - 2))
green_position = (random.randint(1, maze.cols - 2), random.randint(1, maze.rows - 2))

while abs(red_position[0] - green_position[0]) <= 1 and abs(red_position[1] - green_position[1]) <= 1:
    red_position = (random.randint(1, maze.cols - 2), random.randint(1, maze.rows - 2))
    green_position = (random.randint(1, maze.cols - 2), random.randint(1, maze.rows - 2))

red_balls[0].x, red_balls[0].y = red_position
green_ball.x, green_ball.y = green_position

# loop utama (Perulangan utama yang menjalankan game hingga kondisi berhenti terpenuhi.)
running = True
while running:
    screen.fill(WHITE)

# untuk menghandle event event yang terjadi dalam game (Jika event QUIT terdeteksi, perulangan utama akan berhenti dan
# permainan akan ditutup. Jika event MOUSEBUTTONDOWN terdeteksi, akan dilakukan penanganan klik pada tombol-tombol dan objek-objek permainan.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if start_button_rect.collidepoint(event.pos):
                    for ball in red_balls:
                        ball.is_paused = False
                    green_ball.is_paused = False
                elif pause_button_rect.collidepoint(event.pos):
                    for ball in red_balls:
                        ball.is_paused = True
                    green_ball.is_paused = True
                elif shuffle_red_button_rect.collidepoint(event.pos):
                    for ball in red_balls:
                        ball.x = random.randint(1, maze.cols - 2)
                        ball.y = random.randint(1, maze.rows - 2)
                elif shuffle_green_button_rect.collidepoint(event.pos):
                    green_ball.x = random.randint(1, maze.cols - 2)
                    green_ball.y = random.randint(1, maze.rows - 2)
                elif shuffle_map_button_rect.collidepoint(event.pos):
                    maze.shuffle_map()
                elif red_view_button_rect.collidepoint(event.pos):
                    show_red_view = not show_red_view
                elif add_button.rect.collidepoint(event.pos):
                    add_button.handle_click()
                elif remove_button.rect.collidepoint(event.pos):
                    remove_button.handle_click()

    maze.draw()
    if not show_red_view:
        green_ball.auto_move()
        green_ball.draw()

    for ball in red_balls:
        ball.auto_move()
        ball.draw()

    if any(ball.x == green_ball.x and ball.y == green_ball.y for ball in red_balls):
        running = False

# menggambar tombol
    pygame.draw.rect(screen, BLUE, start_button_rect)
    pygame.draw.rect(screen, BLUE, pause_button_rect)
    pygame.draw.rect(screen, BLUE, shuffle_red_button_rect)
    pygame.draw.rect(screen, BLUE, shuffle_green_button_rect)
    pygame.draw.rect(screen, BLUE, shuffle_map_button_rect)
    pygame.draw.rect(screen, BLUE, red_view_button_rect)

    for ball in red_balls:
        ball.draw()
    green_ball.draw()

    add_button.draw()
    remove_button.draw()

# untuk menggambar label/tulisan di tombol
    font = pygame.font.Font(None, 20)
    start_text = font.render("     MULAI", True, WHITE)
    pause_text = font.render("  BERHENTI", True, WHITE)
    shuffle_red_text = font.render("    ACAK MERAH", True, WHITE) 
    shuffle_green_text = font.render("      ACAK HIJAU", True, WHITE)
    shuffle_map_text = font.render("       ACAK PETA", True, WHITE) 
    red_view_text = font.render("POV DROID MERAH", True, WHITE)

# menggambar semua objek permainan pada layar
    screen.blit(start_text, (860, 30))
    screen.blit(pause_text, (860, 80))
    screen.blit(shuffle_red_text, (840, 130))
    screen.blit(shuffle_green_text, (835, 180))
    screen.blit(shuffle_map_text, (835, 230))
    screen.blit(red_view_text, (840, 280))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
