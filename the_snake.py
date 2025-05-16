"""Памагите!!!"""
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
import random
import pygame


# Константы
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20  # размер ячейки игрового поля
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


class GameObject(ABC):
    """Базовый класс для игровых объектов."""

    def __init__(self, position: Tuple[int, int]) -> None:
        """Инициализация базовых атрибутов объекта."""
        self.position = position
        self.body_color: Optional[Tuple[int, int, int]] = None

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Метод для отрисовки объекта."""


class Apple(GameObject):
    """Класс яблока в игре."""

    body_color = (255, 0, 0)  # красный цвет яблока

    def __init__(self) -> None:
        """Инициализация яблока с случайной позицией."""
        # Сразу задаём случайную позицию
        super().__init__(self.randomize_position())

    def randomize_position(self) -> Tuple[int, int]:
        """Устанавливает случайную позицию яблока на игровом поле."""
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return x, y

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает яблоко на поверхности."""
        rect = pygame.Rect(self.position[0] * GRID_SIZE,
                           self.position[1] * GRID_SIZE,
                           GRID_SIZE,
                           GRID_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки."""

    body_color = (0, 255, 0)  # зелёный цвет змейки

    def __init__(self) -> None:
        """Инициализация змейки в центре экрана с длиной 1."""
        center_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        super().__init__(center_pos)
        self.length = 1
        self.positions: List[Tuple[int, int]] = [center_pos]
        self.direction = (1, 0)  # изначально движемся вправо
        self.next_direction: Optional[Tuple[int, int]] = None

    def update_direction(self) -> None:
        """Обновляет направление змейки."""
        if self.next_direction:
            # Не даём змейке двигаться в обратном направлении
            opposite = (-self.direction[0], -self.direction[1])
            if self.next_direction != opposite:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Передвигает змейку в новом направлении."""
        current_head = self.positions[0]
        new_head = ((current_head[0] + self.direction[0]) % GRID_WIDTH,
                    (current_head[1] + self.direction[1]) % GRID_HEIGHT)

        # Вставляем новую голову
        self.positions.insert(0, new_head)

        # Если длина змейки не увеличилась, удаляем последний элемент
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает змейку на поверхности."""
        for pos in self.positions:
            rect = pygame.Rect(pos[0] * GRID_SIZE,
                               pos[1] * GRID_SIZE,
                               GRID_SIZE,
                               GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)

    def get_head_position(self) -> Tuple[int, int]:
        """
        Возвращает позицию головы змейки.

        Returns:
            Позиция головы (x, y).
        """
        return self.positions[0]

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        center_pos = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.length = 1
        self.positions = [center_pos]
        self.direction = (1, 0)
        self.next_direction = None


def handle_keys(snake: Snake) -> None:
    """
    Обрабатывает нажатия клавиш и меняет направление змейки.

    Args:
        snake: объект змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # pylint: disable=no-member
            pygame.quit()  # pylint: disable=no-member
            exit()
        elif event.type == pygame.KEYDOWN:  # pylint: disable=no-member
            if event.key == pygame.K_UP:  # pylint: disable=no-member
                snake.next_direction = (0, -1)
            elif event.key == pygame.K_DOWN:  # pylint: disable=no-member
                snake.next_direction = (0, 1)
            elif event.key == pygame.K_LEFT:  # pylint: disable=no-member
                snake.next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT:  # pylint: disable=no-member
                snake.next_direction = (1, 0)


def main() -> None:
    """
    Основная функция игры, где происходит инициализация,
    игровой цикл, обновление и отрисовка объектов.
    """
    pygame.init()  # pylint: disable=no-member
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')

    clock = pygame.time.Clock()
    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверяем, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            # Устанавливаем яблоко в новую случайную позицию,
            # которая не совпадает с позицией змейки
            while True:
                apple.position = apple.randomize_position()
                if apple.position not in snake.positions:
                    break

        # Проверяем столкновение змейки с собой
        head = snake.get_head_position()
        if head in snake.positions[1:]:
            snake.reset()

        screen.fill((0, 0, 0))  # очистка экрана (чёрный цвет)
        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()
        clock.tick(10)  # FPS (скорость игры)


if __name__ == '__main__':
    main()
