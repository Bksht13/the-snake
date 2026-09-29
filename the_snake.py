from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
# Константа координат центральной клетки в пикселях:
CENTER_POSITION = (
    (GRID_WIDTH // 2) * GRID_SIZE,
    (GRID_HEIGHT // 2) * GRID_SIZE
)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс игровых объектов"""

    def __init__(self, position=CENTER_POSITION, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки объектов"""
        raise NotImplementedError('Метод не переопределён')


class Apple(GameObject):
    """Класс игрового объекта яблоко"""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.position = None

    def randomize_position(self, snake_positions):
        """Метод определяет случайную позицию яблока"""
        while True:
            self.position = (
                GRID_SIZE * randint(0, GRID_WIDTH - 1),
                GRID_SIZE * randint(0, GRID_HEIGHT - 1)
            )
            if self.position not in snake_positions:
                return

    def draw(self):
        """Метод отрисовывает яблоко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(
            screen,
            self.body_color,
            rect
        )
        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            rect,
            1
        )


class Snake(GameObject):
    """Класс игрового объекта змейка"""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Метод возвращает начальное положение головы змейки"""
        return self.positions[0]

    def update_direction(self):
        """Метод обновляет текущее направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод описывает движение змейки"""
        self.update_direction()
        head_x, head_y = self.get_head_position()
        x, y = self.direction
        new_head = (
            (head_x + x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop()

    def reset(self):
        """Метод описывает последствия столкновения змейки"""
        self.__init__()
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

    def draw(self):
        """Метод отрисовывает объект змейка"""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(
                screen,
                self.body_color,
                rect
            )
            pygame.draw.rect(
                screen,
                BORDER_COLOR,
                rect,
                1
            )


def handle_keys(game_object):
    """Функция отвечает за изменение направления змейки"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция описывает основной игровой цикл"""
    # Инициализация PyGame:
    pygame.init()
    apple = Apple()
    snake = Snake()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
