from collections import deque


class Snake:
    directions = {0: (0, -1),  # up
                  1: (1, 0),  # right
                  2: (0, 1),  # down
                  3: (-1, 0)}  # left

    def __init__(self,
                 start_x: int,
                 start_y: int,
                 start_length: int = 5,
                 start_direction: int = 1) -> None:

        self.x = deque([start_x - self.directions[start_direction][0] * i for i in range(start_length)])
        self.y = deque([start_y - self.directions[start_direction][1] * i for i in range(start_length)])
        self.length = start_length
        self._direction = start_direction
        self._prev_direction = start_direction

    def update_direction(self, value: int) -> None:
        if value not in range(4):
            raise ValueError("Direction must be 0, 1, 2 or 3")
        if value == self._direction or (value + self._prev_direction) % 2 == 0:
            # Prevents snake from turning 180 degrees
            return
        self._direction = value

    def move(self) -> None:
        self.x.appendleft(self.x[0] + self.directions[self._direction][0])
        self.y.appendleft(self.y[0] + self.directions[self._direction][1])
        self._prev_direction = self._direction
        if len(self.body) > self.length:
            self.x.pop()
            self.y.pop()

    @property
    def body(self):
        return list(zip(self.x, self.y))

    @property
    def head(self):
        return self.x[0], self.y[0]
