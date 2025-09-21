from random import randint

import sys

import pygame as pg

# Цвета RGB
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
CYAN = (93, 216, 228)
WHITE = (255, 255, 255)

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
START_SNAKE_X = (GRID_WIDTH // 2) * GRID_SIZE
START_SNAKE_Y = (GRID_HEIGHT // 2) * GRID_SIZE
START_SNAKE_POSITION = (START_SNAKE_X, START_SNAKE_Y)


# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = BLACK
BORDER_COLOR = CYAN
APPLE_COLOR = RED
SNAKE_COLOR = GREEN

# Скорость движения змейки (FPS)
SPEED = 20

DEFAULT_POSITION = (0, 0)
DEFAULT_COLOR = BOARD_BACKGROUND_COLOR

# Настройка игрового окна
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=DEFAULT_POSITION, body_color=DEFAULT_COLOR):
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position, color, border_color=BORDER_COLOR):
        """Отрисовает 1 клетку на экране"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, border_color, rect, 1)

    def draw(self):
        """Метод отрисовки. Должен быть переопределён в наследниках."""
        raise NotImplementedError


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, position=None, body_color=APPLE_COLOR,
                 occupied_positions=None):
        if position is None:
            position = (0, 0)
        super().__init__(position, body_color)
        if position == (0, 0):
            self.randomize_position()

    def randomize_position(self, occupied_positions=None):
        """Устанавливает случайную позицию яблока."""
        if occupied_positions is None:
            occupied_positions = []

        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (x, y)
            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает яблоко."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self, position=START_SNAKE_POSITION, body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.reset()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self, new_direction=None):
        """Обновляет направление движения змейки.

        Если передан new_direction — обновляем направление,
        если нет — используем self.next_direction.
        """
        if new_direction:
            opposite = (-self.direction[0], -self.direction[1])
            if new_direction != opposite:
                self.direction = new_direction
            self.next_direction = None
        elif self.next_direction:
            opposite = (-self.direction[0], -self.direction[1])
            if self.next_direction != opposite:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Передвигает змейку по экрану."""
        cur = self.get_head_position()
        x, y = self.direction
        new_pos = (
            (cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
            (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_pos)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает всю змейку на экране."""
        for pos in self.positions:
            self.draw_cell(pos, self.body_color)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.position = START_SNAKE_POSITION
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            new_direction = None
            if event.key == pg.K_UP:
                new_direction = UP
            elif event.key == pg.K_DOWN:
                new_direction = DOWN
            elif event.key == pg.K_LEFT:
                new_direction = LEFT
            elif event.key == pg.K_RIGHT:
                new_direction = RIGHT
            if new_direction:
                snake.update_direction(new_direction)


def main():
    """Основная функция запуска игры."""
    pg.init()
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head = snake.get_head_position()
        if head in snake.positions[1:]:
            snake.reset()

        if head == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
