import logging

logger = logging.getLogger(f"snake_game.{__name__}")

class Apple:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        logger.debug(f"Apple created at position ({self.x}, {self.y})")
