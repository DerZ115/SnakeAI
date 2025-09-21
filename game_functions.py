import logging
import random
import pygame
import sys
import numpy as np

from itertools import product
from snake import Snake
from apple import Apple
from config import Config

logger = logging.getLogger(f"snake_game.{__name__}")

def check_events(snake: Snake, apple: Apple) -> None:
    """Check for events and update snake direction accordingly"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.direction = 0
                logger.debug("Right input")
            elif event.key == pygame.K_DOWN:
                snake.direction = 1
                logger.debug("Down input")
            elif event.key == pygame.K_LEFT:
                snake.direction = 2
                logger.debug("Left input")
            elif event.key == pygame.K_UP:
                snake.direction = 3
                logger.debug("Up input")
            

def draw_entities(screen: pygame.Surface, snake: Snake, apple: Apple) -> None:
    """Draw snake and apple on screen"""
    logger.debug("Drawing snake head")
    pygame.draw.rect(screen, Config.SNAKE_HEAD_COLOR, (snake.x[0] * Config.SCALE + 0.05 * Config.SCALE,
                                                       snake.y[0] * Config.SCALE + 0.05 * Config.SCALE,
                                                       Config.SCALE * 0.9, Config.SCALE * 0.9))
    logger.debug("Drawing snake body")
    for coord in snake.body[1:]:
        pygame.draw.rect(screen, Config.SNAKE_COLOR, (coord[0] * Config.SCALE + 0.05 * Config.SCALE,
                                                      coord[1] * Config.SCALE + 0.05 * Config.SCALE,
                                                      Config.SCALE * 0.9, Config.SCALE * 0.9))
    logger.debug("Drawing apple")
    pygame.draw.rect(screen, Config.FOOD_COLOR, (apple.x * Config.SCALE + 0.05 * Config.SCALE,
                                                 apple.y * Config.SCALE + 0.05 * Config.SCALE,
                                                 Config.SCALE * 0.9, Config.SCALE * 0.9))


def check_collision(snake: Snake, max_x: int, max_y: int) -> bool:
    """Check if snake collides with itself or the edges of the screen"""
    if snake.head in snake.body[1:]:
        logger.debug("Snake collided with itself")
        return True
    if snake.head[0] < 0 or snake.head[0] >= max_x or \
       snake.head[1] < 0 or snake.head[1] >= max_y:
        logger.debug("Snake collided with wall")
        return True
    return False


def check_food_collision(snake: Snake, apple: Apple) -> bool:
    """Check if snake collides with apple and update snake length accordingly"""
    if snake.head == (apple.x, apple.y):
        snake.length += 1
        logger.debug("Snake ate apple")
        return True
    return False


def spawn_apple(snake: Snake, max_x: int, max_y: int) -> Apple | None:
    """Spawn apple at random location that is not occupied by snake"""
    body = set(snake.body)
    possible_spawns = [tpl for tpl in product(range(max_x), range(max_y)) if tpl not in body]
    
    if not possible_spawns:
        logger.warning("No possible spawns for apple")
        return None
    return Apple(*random.choice(possible_spawns))
        

def get_inputs(snake: Snake, apple: Apple):
    """Get inputs for AI decision-making"""
    rotation_matrices = [np.array([[1, 0],
                                   [0, 1]]), # Right
                         np.array([[0, 1],
                                   [-1, 0]]), # Down
                         np.array([[-1, 0],
                                   [0, -1]]), # Left
                         np.array([[0, -1],
                                   [1, 0]])] # Up 
    
    head_coord = np.array(snake.head)
    apple_coord = np.array([apple.x, apple.y])
    body_coord = np.array(snake.body[1:])
    direction = snake.direction
    
    dist_apple_fb, dist_apple_rl = rotation_matrices[direction] @ (apple_coord - head_coord)
    dist_wall = np.array([Config.GAME_WIDTH - head_coord[0],  # Right
                          Config.GAME_HEIGHT - head_coord[1], # Down
                          head_coord[0] + 1,                  # Left
                          head_coord[1] + 1])                 # Up
    
    dist_wall_front = dist_wall[direction]
    dist_wall_left = dist_wall[(direction + 3) % 4]
    dist_wall_right = dist_wall[(direction + 1) % 4]    
    dist_body = (rotation_matrices[direction] @ (body_coord - head_coord).T).T
    
    dist_body_front = min([x[0] for x in dist_body if x[1] == 0 and x[0] > 0], default=dist_wall_front)
    dist_body_left = min([abs(x[1]) for x in dist_body if x[0] == 0 and x[1] < 0], default=dist_wall_left)
    dist_body_right = min([x[1] for x in dist_body if x[0] == 0 and x[1] > 0], default=dist_wall_right)

    return np.array([dist_apple_fb, dist_apple_rl, 
                     dist_wall_front, dist_wall_left, dist_wall_right, 
                     dist_body_front, dist_body_left, dist_body_right])


def run_game(screen: pygame.Surface,
             clock: pygame.time.Clock,
             snake: Snake,
             apple: Apple,):
    """Main game loop"""
    logger.debug("Initializing score")
    score = 0

    logger.debug("Drawing initial entities")

    screen.fill(Config.BG_COLOR)
    draw_entities(screen, snake, apple)
    pygame.display.flip()

    while True:
        
        if Config.AI:
            ai_inputs = get_inputs(snake, apple)
            logger.debug(f"Getting AI inputs")
            logger.debug(ai_inputs)
            
            # TODO: Integrate AI decision-making here
        else:
            check_events(snake, apple)
            
        snake.move()
        if check_food_collision(snake, apple):
            score += 1
            apple_tmp = spawn_apple(snake, Config.GAME_WIDTH, Config.GAME_HEIGHT)
            if apple_tmp is None:
                logger.info("No more space for apple, you win!")
                break
            apple = apple_tmp

        if check_collision(snake, Config.GAME_WIDTH, Config.GAME_HEIGHT):
            break
        
        screen.fill(Config.BG_COLOR)
        draw_entities(screen, snake, apple)
        logger.debug("Updating display")
        pygame.display.update()
        clock.tick(Config.SPEED)

    screen.fill(Config.BG_COLOR)
    
    return score


def run_game_headless(snake: Snake,
                      apple: Apple,):
    """Main game loop"""
    logger.debug("Initializing score")
    score = 0

    while True:
        
        ai_inputs = get_inputs(snake, apple)
        logger.debug(f"Getting AI inputs")
        logger.debug(ai_inputs)
        
        # TODO: Integrate AI decision-making here
            
        snake.move()
        
        if check_food_collision(snake, apple):
            score += 1
            apple_tmp = spawn_apple(snake, Config.GAME_WIDTH, Config.GAME_HEIGHT)
            if apple_tmp is None:
                logger.info("No more space for apple, you win!")
                break
            apple = apple_tmp

        if check_collision(snake, Config.GAME_WIDTH, Config.GAME_HEIGHT):
            break

    return score