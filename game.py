import os
import pygame
import sys
import time
import os

import paddle

os.environ['SDL_VIDEO_CENTERED'] = '1'

GRID_ENABLED = True

class PyBreak:

    def __init__(self):
        """
        PyBreak, a clone of Breakout.
        :return:
        """

        pygame.init()

        # game settings

        self.display = pygame.display.Info()

        self.window_width = 640
        self.window_height = 640

        self.grid_size = 40
        self.grid_x = self.window_width / self.grid_size
        self.grid_y = self.window_height / self.grid_size

        self.fps = 60

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        # paddle settings

        self.start_point = self.grid_x * 18, self.grid_y * 34

        self.paddle = paddle.Paddle()
        self.paddle.size(self.grid_x * 4, self.grid_y)
        self.paddle.step(self.grid_x)
        self.paddle.position(*self.start_point)
        self.paddle.colour((150, 75, 25))

        self.boundary_left = 0
        self.boundary_right = self.window_width - self.paddle.size()[0]

    def main_loop(self):
        """
        Main game loop.
        :return:
        """
        st = time.time()

        key_time = 0
        key_delay = 0.027

        direction = None

        while True:
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    key_time = time.time()
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

                    if event.key == pygame.K_f:
                        pygame.display.toggle_fullscreen()

                    if event.key == pygame.K_RIGHT:
                        direction = self.paddle.direction.RIGHT
                    if event.key == pygame.K_LEFT:
                        direction = self.paddle.direction.LEFT

                if event.type == pygame.KEYUP:
                    direction = None

            pygame.time.Clock().tick(self.fps)

            if GRID_ENABLED is True:
                for x in range(self.grid_size):
                    for y in range(self.grid_size):
                        pygame.draw.rect(self.screen, (100, ) * 3, (
                            0 + self.grid_x * x, 0 + self.grid_y * y,
                            self.grid_x, self.grid_y
                        ), 1)

            # paddle operation

            # paddle boundary detection
            if direction is self.paddle.direction.LEFT and \
                    self.paddle.position()[0] == self.boundary_left or \
                    direction is self.paddle.direction.RIGHT and \
                    self.paddle.position()[0] == self.boundary_right:
                move = False
            else:
                move = True

            if time.time() - key_time > key_delay and move is True:
                self.paddle.move(direction)

            pygame.draw.rect(self.screen, *self.paddle.render())

            pygame.display.flip()

if __name__ == "__main__":
    pb = PyBreak()
    pb.main_loop()
