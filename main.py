import pygame

import game_functions as gf

from snake import Snake
from config import Config

pygame.init()
pygame.display.set_caption("Snake")

screen = pygame.display.set_mode((Config.GAME_WIDTH * Config.SCALE,
                                  Config.GAME_HEIGHT * Config.SCALE))

snake = Snake(Config.GAME_WIDTH // 2, Config.GAME_HEIGHT // 2)
apple = gf.spawn_apple(snake, Config.GAME_WIDTH, Config.GAME_HEIGHT)
clock = pygame.time.Clock()

score = gf.run_game(screen, clock, snake, apple)

print(f"Your score is {score}")
