import random
import pygame
import sys

from snake import Snake
from apple import Apple
from config import Config


def check_events(snake: Snake) -> None:
    """Check for events and update snake direction accordingly"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(0)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(1)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(2)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(3)


def draw_entities(screen: pygame.Surface, snake: Snake, apple: Apple) -> None:
    """Draw snake and apple on screen"""
    pygame.draw.rect(screen, Config.SNAKE_HEAD_COLOR, (snake.x[0] * Config.SCALE,
                                                       snake.y[0] * Config.SCALE,
                                                       Config.SCALE, Config.SCALE))
    for coord in snake.body[1:]:
        pygame.draw.rect(screen, Config.SNAKE_COLOR, (coord[0] * Config.SCALE,
                                                      coord[1] * Config.SCALE,
                                                      Config.SCALE, Config.SCALE))
    pygame.draw.rect(screen, Config.FOOD_COLOR, (apple.x * Config.SCALE,
                                                 apple.y * Config.SCALE,
                                                 Config.SCALE, Config.SCALE))


def check_collision(snake: Snake, max_x: int, max_y: int) -> bool:
    """Check if snake collides with itself or the edges of the screen"""
    if snake.head in snake.body[1:] or \
       snake.head[0] < 0 or snake.head[0] >= max_x or \
       snake.head[1] < 0 or snake.head[1] >= max_y:
        return True
    return False


def check_food_collision(snake: Snake, apple: Apple) -> bool:
    """Check if snake collides with apple and update snake length accordingly"""
    if snake.head == (apple.x, apple.y):
        snake.length += 1
        return True
    return False


def spawn_apple(snake: Snake, max_x: int, max_y: int) -> Apple:
    """Spawn apple at random location that is not occupied by snake"""
    while True:
        x = random.randint(0, max_x - 1)
        y = random.randint(0, max_y - 1)
        if (x, y) not in snake.body:
            return Apple(x, y)


def run_game(screen: pygame.Surface,
             clock: pygame.time.Clock,
             snake: Snake,
             apple: Apple,):
    """Main game loop"""
    score = 0

    screen.fill(Config.BG_COLOR)
    draw_entities(screen, snake, apple)
    pygame.display.flip()

    while True:
        check_events(snake)
        screen.fill(Config.BG_COLOR)
        snake.move()
        if check_food_collision(snake, apple):
            score += 1
            apple = spawn_apple(snake, Config.GAME_WIDTH, Config.GAME_HEIGHT)
        if check_collision(snake, Config.GAME_WIDTH, Config.GAME_HEIGHT):
            break
        draw_entities(screen, snake, apple)
        pygame.display.update()

        clock.tick(Config.SPEED)

    screen.fill(Config.BG_COLOR)
    print("Game Over")
    return score
