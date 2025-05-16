"""Надоело все."""
from random import randint
import pygame

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость змейки
SPEED = 20

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()


class Apple:
    """Класс, представляющий яблоко на игровом поле."""

    def __init__(self):
        """Инициализирует яблоко и задаёт его случайную позицию."""
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Генерирует новую случайную позицию для яблока."""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake:
    """Класс, представляющий змею."""

    def __init__(self):
        """Инициализирует змею и задаёт начальные параметры."""
        self.body_color = SNAKE_COLOR
        self.positions = [(100, 100)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def move(self):
        """Обновляет положение змеи на игровом поле."""
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions = [new_head] + self.positions
        self.last = self.positions.pop()

    def update_direction(self):
        """Обновляет направление змеи при изменении направления движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовывает змею на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def grow(self):
        """Добавляет сегмент к змее."""
        if self.last:
            self.positions.append(self.last)
            self.last = None


def handle_keys(game_object):
    """Обрабатывает события клавиатуры и выход из игры."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # pylint: disable=no-member
            pygame.quit()  # pylint: disable=no-member
            raise SystemExit
        elif event.type == pygame.KEYDOWN:  # pylint: disable=no-member
            if (
                event.key == pygame.K_UP  # pylint: disable=no-member
                and game_object.direction != DOWN
            ):
                game_object.next_direction = UP
            elif (event.key == pygame.K_DOWN  # pylint: disable=no-member
                  and game_object.direction != UP):
                game_object.next_direction = DOWN
            elif (event.key == pygame.K_LEFT  # pylint: disable=no-member
                  and game_object.direction != RIGHT):
                game_object.next_direction = LEFT
            elif (event.key == pygame.K_RIGHT  # pylint: disable=no-member
                  and game_object.direction != LEFT):
                game_object.next_direction = RIGHT


def main():
    """Главная функция запуска игры."""
    pygame.init()  # pylint: disable=no-member
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # 🍏 Проверка на съедение яблока
        if snake.positions[0] == apple.position:
            snake.grow()
            apple.position = apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
