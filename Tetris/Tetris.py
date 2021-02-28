import pygame
from random import choice


A = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

B = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

C = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

D = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

E = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

F = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

G = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
# шаблоны фигур

figures = [A, B, C, D, E, F, G]
figure_colors = [(255, 0, 255), (255, 0, 0), (50, 255, 50), (128, 0, 128), (0, 0, 255), (255, 255, 0), (0, 255, 255)]
s_width = 800
s_height = 700
play_width = 300
play_height = 600  
size = 30
top_left_x = (s_width - play_width) // 2 - 200
top_left_y = s_height - play_height
# основные глобальные переменные


class Figure: 
    def __init__(self, x, y, form):
        self.x = x
        self.y = y
        self.form = form
        self.color = figure_colors[figures.index(form)]
        self.rotation = 0
# класс, в котором заданы основные параметры фигур


def create_grid(locked_positions={}):  
    grid = [[(0, 0, 0) for columns in range(10)] for rows in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid
# создание сетки


def draw_grid(surface, grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, ('white'), (top_left_x + j * size, top_left_y + i * size, size, size), width=1)
# рисование сетки


def get_figure():
    return Figure(5, 0, choice(figures))
# получение случайной фигуры


def draw_next_figure(figure, surface):
    sx = top_left_x + play_width + 270
    sy = top_left_y + play_height / 2 - 300
    form = figure.form[figure.rotation % len(figure.form)]

    x = top_left_x + play_width + 50
    draw_text(surface, 'Следующая фигура:', 20, ('white') ,x, sy + 50)

    for i, line in enumerate(form):
        for j, column in enumerate(list(line)):
            if column == '0':
                pygame.draw.rect(surface, figure.color, (sx + j * size, sy + i * size, size, size))
                pygame.draw.rect(surface, ('white'), (sx + j * size, sy + i * size, size, size), width=1)
# рисование следующей фигуры(справа вверху)


def change_form(figure):
    positions = []
    form = figure.form[figure.rotation % len(figure.form)]

    for i, line in enumerate(form):
        for j, column in enumerate(list(line)):
            if column == '0':
                positions.append((figure.x + j, figure.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions
# превращение основного шаблона в более удобный формат


def free_place(figure, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    formatted = change_form(figure)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True
# проверка, есть ли свободное место возле фигуры


def clear_rows(grid, locked):
    count = 0
    for i in range(len(grid) - 1, -1, -1):
        if (0, 0, 0) not in grid[i]:
            count += 1
            ind = i
            for j in range(len(grid[i])):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if count > 0:
        for old in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = old
            if y < ind:
                new = (x, y + count)
                locked[new] = locked.pop(old)

    return count
# очищает заполненные линии


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False
# проверка на проигрыш


def max_score():
    with open('data/scores.txt', 'r', encoding='utf8') as file:
        score = file.readlines()[0].strip()
    return score
# взятие счета из файла


def update_score(nscore):
    score = max_score()
    with open('data/scores.txt', 'w', encoding='utf8') as f:
        if int(score) > nscore:
            f.write(score)
        else:
            f.write(str(nscore))
# записывание счета в файл


def draw_window(surface, grid, score=0, last_score = 0):
    x, y = s_width // 3, s_height // 30
    draw_text(surface, 'Тетрис', 50, ('white'), x, y)

    x, y = s_width - 400, s_height - 500
    draw_text(surface, 'Счёт:', 20, ('white'), x, y)
    draw_text(surface, str(score), 20, ('white'), x + 100, y)

    draw_text(surface, 'Лучший счёт:', 20, ('white'), x, y + 50)
    draw_text(surface, str(last_score), 20, ('white'), x + 200, y + 50)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * size, top_left_y + i * size, size, size))

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), width=5)
    draw_grid(surface, grid)
# рисование основного окна со всеми элементами


def draw_text(surface, text, size, color, x, y):
    font = pygame.font.SysFont('verdana', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (x, y))
# функция для рисования текста


def draw_main_menu(surface):
    draw_text(surface, 'Добро пожаловать в игру тетрис!', 20, ('white'), s_width // 4, s_height // 10)
    draw_text(surface, 'Цель игры - заполнять падающими', 18, ('white'), s_width // 4, s_height // 6 + 20)
    draw_text(surface, 'фигурами все клетки в строке', 18, ('white'), s_width // 4 + 20, s_height // 4 - 20)
    draw_text(surface, 'Управление:', 18, ('white'), s_width // 4, s_height // 4 + 40)
    draw_text(surface, 'W - поворот фигуры', 18, ('white'), s_width // 4 + 20, s_height // 4 + 80)
    draw_text(surface, 'A - на одну клетку влево', 18, ('white'), s_width // 4 + 20, s_height // 4 + 100)
    draw_text(surface, 'S - на одну клетку вниз', 18, ('white'), s_width // 4 + 20, s_height // 4 + 120)
    draw_text(surface, 'D - на одну клетку вправо', 18, ('white'), s_width // 4 + 20, s_height // 4 + 140)
    draw_text(surface, 'Для продолжения нажмите любую кнопку', 20, ('white'), s_width // 5, s_height - 200)


def game(screen):
    game_music = pygame.mixer.Sound('data/music/game.mp3')
    game_music.play(-1)
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_figure = False
    running = True
    figure = get_figure()
    next_figure = get_figure()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.3
    level_time = 0
    score = 0

    while running:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            figure.y += 1
            if not free_place(figure, grid) and figure.y > 0:
                figure.y -= 1
                change_figure = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_music.stop()
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    figure.x -= 1
                    if not free_place(figure, grid):
                        figure.x += 1
                if event.key == pygame.K_d:
                    figure.x += 1
                    if not free_place(figure, grid):
                        figure.x -= 1
                if event.key == pygame.K_s:
                    figure.y += 1
                    if not free_place(figure, grid):
                        figure.y -= 1
                if event.key == pygame.K_w:
                    figure.rotation += 1
                    if not free_place(figure, grid):
                        figure.rotation -= 1

        form_pos = change_form(figure)

        for i in range(len(form_pos)):
            x, y = form_pos[i]
            if y > -1:
                grid[y][x] = figure.color

        if change_figure:
            for pos in form_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = figure.color
            figure = next_figure
            next_figure = get_figure()
            change_figure = False
            score += clear_rows(grid, locked_positions) * 10

        screen.fill((0, 0, 0))
        draw_window(screen, grid, score, last_score)
        draw_next_figure(next_figure, screen)
        update_score(score)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text(screen, 'Вы проиграли!', 60, ('white'), s_width // 6, s_height // 2)
            pygame.display.update()
            pygame.time.delay(2000)
            game_music.stop()
            running = False
# основная функция, где выполняется игра


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Тетрис')
    main_menu_music = pygame.mixer.Sound('data/music/main_menu.mp3')
    main_menu_music.play(-1)
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_main_menu(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu_music.stop()
                running = False
            if event.type == pygame.KEYDOWN:
                main_menu_music.stop()
                game(screen)
    pygame.quit()
# функция главного меню


if __name__ == '__main__':
    main_menu()