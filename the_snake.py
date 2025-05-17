"""Памагите!!!"""
from random import randint
import pygame

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Класс GameObject"""

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовка."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс Apple."""

    def __init__(self):
        position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                    randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        super().__init__(position, APPLE_COLOR)

    def randomize_position(self, occupied_positions):
        """Позиция."""
        while True:
            new_pos = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                       randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_pos not in occupied_positions:
                self.position = new_pos
                break


class Snake(GameObject):
    """Класс Snake."""

    def __init__(self, x, y):
        super().__init__(x, y)
        self.positions = [(GRID_SIZE * 5, GRID_SIZE * 12)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """."""
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        if new_head in self.positions:
            raise RuntimeError("Game Over")

        self.positions = [new_head] + self.positions[:-1]

    def grow(self):
        """."""
        tail = self.positions[-1]
        self.positions.append(tail)

    def draw(self):
        """."""
        for pos in self.positions:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def handle_keys(self):
        """."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                pygame.quit()  # pylint: disable=no-member
                raise SystemExit
            elif event.type == pygame.KEYDOWN:  # pylint: disable=no-member
                if (
                    event.key == pygame.K_UP  # pylint: disable=no-member
                    and self.direction != DOWN
                ):
                    self.next_direction = UP
                elif (
                    event.key == pygame.K_DOWN  # pylint: disable=no-member
                    and self.direction != UP
                ):
                    self.next_direction = DOWN
                elif (
                    event.key == pygame.K_LEFT  # pylint: disable=no-member
                    and self.direction != RIGHT
                ):
                    self.next_direction = LEFT
                elif (event.key == pygame.K_RIGHT  # pylint: disable=no-member
                      and self.direction != LEFT
                      ):
                    self.next_direction = RIGHT


def main():
    """."""
    pygame.init()  # pylint: disable=no-member
    snake = Snake(1, 1)
    apple = Apple()

    while True:
        clock.tick(SPEED)
        snake.handle_keys()
        snake.update_direction()

        try:
            snake.move()
        except (ValueError, AttributeError):
            pygame.quit()  # pylint: disable=no-member
            return

        if snake.positions[0] == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
