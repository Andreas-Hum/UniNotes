import pygame
import random
import threading
import queue
import math
from search import SnakeAI

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
GRAY = (40, 40, 40)

# Game dimensions
WIDTH, HEIGHT = 1000, 1000
BLOCK_SIZE = 20

# Directions
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class SnakeGame:
    def __init__(self):
        self.width = WIDTH // BLOCK_SIZE
        self.height = HEIGHT // BLOCK_SIZE
        self.snake = [(self.height // 2, self.width // 2)]
        self.food = self._generate_food()
        self.direction = RIGHT
        self.score = 0
        self.is_over = False
        self.food_callback = None
        self.start_callback = None

    def _generate_food(self):
        while True:
            food = (
                random.randint(0, self.height - 1),
                random.randint(0, self.width - 1),
            )
            if food not in self.snake:
                return food

    def step(self):
        if self.is_over:
            return

        head_y, head_x = self.snake[0]

        if self.direction == UP:
            new_head = (head_y - 1, head_x)
        elif self.direction == RIGHT:
            new_head = (head_y, head_x + 1)
        elif self.direction == DOWN:
            new_head = (head_y + 1, head_x)
        elif self.direction == LEFT:
            new_head = (head_y, head_x - 1)

        # Check if snake runs into the wall
        if (
            new_head[0] < 0
            or new_head[0] >= self.height
            or new_head[1] < 0
            or new_head[1] >= self.width
            or new_head in self.snake
        ):
            self.is_over = True
            return

        # Check if snake eats the food
        if new_head == self.food:
            self.snake.insert(0, new_head)
            self.food = self._generate_food()
            self.score += 1
            if self.food_callback:
                self.food_callback(self)
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()

    def change_direction(self, direction):
        if (
            (self.direction == UP and direction != DOWN)
            or (self.direction == DOWN and direction != UP)
            or (self.direction == LEFT and direction != RIGHT)
            or (self.direction == RIGHT and direction != LEFT)
        ):
            self.direction = direction

    def get_state(self):
        grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y, x in self.snake:
            grid[y][x] = 1
        grid[self.food[0]][self.food[1]] = 2  # Represent food with 2
        return {
            "snake": self.snake,
            "food": self.food,
            "score": self.score,
            "is_over": self.is_over,
            "grid": grid,
            "head": self.snake[0],
            "direction": self.direction,
        }

    def render(self, screen):
        screen.fill(BLACK)

        # Draw gridlines
        for x in range(0, WIDTH, BLOCK_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, BLOCK_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

        for y, x in self.snake:
            pygame.draw.rect(
                screen, GREEN, [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE]
            )
        pygame.draw.rect(
            screen,
            RED,
            [
                self.food[1] * BLOCK_SIZE,
                self.food[0] * BLOCK_SIZE,
                BLOCK_SIZE,
                BLOCK_SIZE,
            ],
        )

        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, [0, 0])

        pygame.display.flip()

    def display_game_over(self, screen):
        font = pygame.font.SysFont(None, 50)
        game_over_text = font.render("Game Over", True, RED)
        screen.blit(game_over_text, [WIDTH // 2 - 100, HEIGHT // 2 - 25])
        pygame.display.flip()

    def on_food_eaten(self, callback):
        """Sets a callback function that is called whenever food is eaten."""
        self.food_callback = callback

    def on_game_start(self, callback):
        """Sets a callback function that is called when the game starts."""
        self.start_callback = callback
        if self.start_callback:
            self.start_callback(self)

    def get_possible_moves(self):
        """Returns a list of possible moves in the form (x, y, action)."""
        head_y, head_x = self.snake[0]
        moves = []

        # Check UP
        if head_y > 0 and (head_y - 1, head_x) not in self.snake:
            moves.append((head_y - 1, head_x, UP))

        # Check RIGHT
        if head_x < self.width - 1 and (head_y, head_x + 1) not in self.snake:
            moves.append((head_y, head_x + 1, RIGHT))

        # Check DOWN
        if head_y < self.height - 1 and (head_y + 1, head_x) not in self.snake:
            moves.append((head_y + 1, head_x, DOWN))

        # Check LEFT
        if head_x > 0 and (head_y, head_x - 1) not in self.snake:
            moves.append((head_y, head_x - 1, LEFT))

        return moves

    def distance_to_wall(self, y, x):
        """Calculate the distance from the given position to the nearest wall."""
        distances = [y, self.height - 1 - y, x, self.width - 1 - x]
        return min(distances)

    def distance_to_body(self, y, x):
        """Calculate the distance from the given position to the nearest body segment."""
        distances = [
            math.sqrt((y - sy) ** 2 + (x - sx) ** 2) for sy, sx in self.snake[1:]
        ]
        return min(distances) if distances else float("inf")


def game_loop(snake_game, command_queue, move_event):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    FPS = 60

    while not snake_game.is_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                snake_game.is_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake_game.change_direction(UP)
                elif event.key == pygame.K_RIGHT:
                    snake_game.change_direction(RIGHT)
                elif event.key == pygame.K_DOWN:
                    snake_game.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake_game.change_direction(LEFT)

        if not command_queue.empty():
            command = command_queue.get_nowait()
            snake_game.change_direction(command)

        snake_game.step()
        snake_game.render(screen)
        clock.tick(FPS)

        next_move(snake_game, command_queue, move_event)

    snake_game.display_game_over(screen)
    pygame.quit()


def start_game_thread(snake_game, command_queue, move_event):
    game_thread = threading.Thread(
        target=game_loop, args=(snake_game, command_queue, move_event)
    )
    game_thread.start()
    return game_thread


def next_move(snake_game, command_queue, move_event):
    """Function to choose a valid move for the snake that doesn't result in collision."""
    while not command_queue.empty():
        command_queue.get_nowait()

    ai = SnakeAI()
    solution = ai.find(snake_game.get_state())

    if solution:
        for move in solution:
            command_queue.put(move)
    move_event.set()


if __name__ == "__main__":
    game = SnakeGame()
    command_queue = queue.Queue()
    move_event = threading.Event()

    game.on_game_start(lambda game: next_move(game, command_queue, move_event))
    game.on_food_eaten(lambda game: next_move(game, command_queue, move_event))

    game_thread = start_game_thread(game, command_queue, move_event)

    game_thread.join()
