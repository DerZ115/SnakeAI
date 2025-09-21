from dataclasses import dataclass


@dataclass
class Config:
    GAME_WIDTH: int = 30
    GAME_HEIGHT: int = 30
    SCALE: int = 25
    BG_COLOR: tuple[int, int, int] = (0, 0, 0)
    SNAKE_COLOR: tuple[int, int, int] = (0, 0, 255)
    SNAKE_HEAD_COLOR: tuple[int, int, int] = (0, 255, 0)
    FOOD_COLOR: tuple[int, int, int] = (255, 0, 0)
    SPEED: float = 5
    AI: bool = False
