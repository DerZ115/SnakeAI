import logging
import pygame
import sys

import game_functions as gf

from snake import Snake
from config import Config

logger = logging.getLogger("snake_game")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(log_formatter)

logger.addHandler(console_handler)

pygame.init()
pygame.display.set_caption("Snake")

logger.info("Initializing game entities")
snake = Snake(Config.GAME_WIDTH // 2, Config.GAME_HEIGHT // 2)
apple = gf.spawn_apple(snake, Config.GAME_WIDTH, Config.GAME_HEIGHT)
if apple is None:
    logger.error("Failed to spawn initial apple")
    sys.exit(1)
if Config.SHOW_GAME:
    logger.info("Game display enabled")
    logger.debug("Initializing game window")
    screen = pygame.display.set_mode((Config.GAME_WIDTH * Config.SCALE,
                                      Config.GAME_HEIGHT * Config.SCALE))
    clock = pygame.time.Clock()

    score = gf.run_game(screen, clock, snake, apple)
else:
    logger.info("Game display disabled, running in headless mode")
    score = gf.run_game_headless(snake, apple)
    
logger.info(f"Game Over - Final Score: {score}")
