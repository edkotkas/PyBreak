import pygame
import sys
import time
import os

from items import Item
from levels import Level

os.environ['SDL_VIDEO_CENTERED'] = '1'

GRID_ENABLED = False
GAME_ENABLED = True

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
        self.caption = pygame.display.set_caption("PyBreak - @edkotkas")

        # paddle settings
        self.paddle = Item()

        self.paddle_width = 5

        self.paddle.size(self.grid_x * self.paddle_width, self.grid_y)
        self.paddle.step(self.grid_x)
        self.paddle.position(self.grid_x * 18, self.grid_y * 34)
        self.paddle.colour((150, 75, 25))

        self.paddle_boundary_left = 0
        self.paddle_boundary_right = self.window_width - self.paddle.size()[0]

        # ball settings
        self.ball = Item()
        self.ball.size(self.grid_x, self.grid_y)
        self.ball.step(self.grid_y)
        self.ball.position(self.grid_x * 19, self.grid_y * 30)
        self.ball.colour((255, 0, 100))

        self.ball_boundary_top = 0 - self.ball.size()[1]
        self.ball_boundary_left = 0
        self.ball_boundary_bottom = self.window_height - self.ball.size()[1]
        self.ball_boundary_right = self.window_width - self.ball.size()[0]

        # level settings
        self.level = Level(self.grid_x, self.grid_y)

    def main_loop(self):
        """
        Main game loop.
        :return:
        """
        x, y = 0, 1

        st = time.time()

        key_time = 0
        key_delay = 0.027

        ball_speed = .025

        paddle_direction = None
        ball_direction_y = self.ball.direction.DOWN
        ball_direction_x = self.ball.direction.RIGHT

        while True:
            self.screen.fill((10, 10, 10))

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
                        paddle_direction = self.paddle.direction.RIGHT
                    if event.key == pygame.K_LEFT:
                        paddle_direction = self.paddle.direction.LEFT

                if event.type == pygame.KEYUP:
                    paddle_direction = None

            pygame.time.Clock().tick(self.fps)

            if GRID_ENABLED is True:
                for grid_x in range(self.grid_size):
                    for grid_y in range(self.grid_size):
                        pygame.draw.rect(self.screen, (100, ) * 3, (
                            0 + self.grid_x * grid_x, 0 + self.grid_y * grid_y,
                            self.grid_x, self.grid_y
                        ), 1)

            if GAME_ENABLED is True:
                # paddle boundary detection
                if paddle_direction is self.paddle.direction.LEFT and \
                        self.paddle.position()[x] == self.paddle_boundary_left or \
                        paddle_direction is self.paddle.direction.RIGHT and \
                        self.paddle.position()[x] == self.paddle_boundary_right:
                    move = False
                else:
                    move = True

                # paddle movement timer
                if time.time() - key_time > key_delay and move is True:
                    self.paddle.move(paddle_direction)

                # renders the paddle
                pygame.draw.rect(self.screen, *self.paddle.render())

                # ball direction control
                if self.ball.position()[y] == self.ball_boundary_top and \
                        ball_direction_y is self.ball.direction.UP:
                    ball_direction_y = self.ball.direction.opposite(ball_direction_y)

                if self.ball.position()[x] == self.ball_boundary_left and \
                        ball_direction_x is self.ball.direction.LEFT:
                    ball_direction_x = self.ball.direction.opposite(ball_direction_x)

                if self.ball.position()[x] == self.ball_boundary_right and \
                        ball_direction_x is self.ball.direction.RIGHT:
                    ball_direction_x = self.ball.direction.opposite(ball_direction_x)

                # bottom bounce, for testing
                if self.ball.position()[y] == self.ball_boundary_bottom and \
                        ball_direction_y is self.ball.direction.DOWN:
                    ball_direction_y = self.ball.direction.opposite(ball_direction_y)

                # ball/paddle collision

                if self.ball.position()[y] + self.grid_y == self.paddle.position()[y] and \
                        ball_direction_y is self.ball.direction.DOWN and \
                        self.ball.position()[x] in \
                        range(self.paddle.position()[x] - 10, self.paddle.position()[x] + self.paddle.size()[0] + 10):
                    ball_direction_y = self.ball.direction.opposite(ball_direction_y)

                # ball/block collision
                for bx in self.level.map():

                    # right
                    if self.ball.position()[x] + self.grid_x == bx.position()[x] and \
                            ball_direction_x is self.ball.direction.RIGHT and \
                            self.ball.position()[y] in \
                            range(bx.position()[y], bx.position()[y] + bx.size()[1]):
                        ball_direction_x = self.ball.direction.opposite(ball_direction_x)

                    # left
                    if self.ball.position()[x] - self.grid_x == bx.position()[x] and \
                            ball_direction_x is self.ball.direction.LEFT and \
                            self.ball.position()[y] in \
                            range(bx.position()[y], bx.position()[y] + bx.size()[1]):
                        ball_direction_x = self.ball.direction.opposite(ball_direction_x)

                    # down
                    if self.ball.position()[y] + self.grid_y == bx.position()[y] and \
                            ball_direction_y is self.ball.direction.DOWN and \
                            self.ball.position()[x] in \
                            range(bx.position()[x], bx.position()[x] + bx.size()[0]):
                        ball_direction_y = self.ball.direction.opposite(ball_direction_y)

                    # up
                    if self.ball.position()[y] - self.grid_y == bx.position()[y] and \
                            ball_direction_y is self.ball.direction.UP and \
                            self.ball.position()[x] in \
                            range(bx.position()[x], bx.position()[x] + bx.size()[0]):
                        ball_direction_y = self.ball.direction.opposite(ball_direction_y)
                        self.level.hit(bx)

                # ball movement control
                if time.time() - st > ball_speed:
                    st = time.time()
                    self.ball.move(ball_direction_y)
                    self.ball.move(ball_direction_x)

                # renders the ball
                pygame.draw.rect(self.screen, *self.ball.render())

            for b in self.level.map():
                pygame.draw.rect(self.screen, *b.render())

            pygame.display.flip()

if __name__ == "__main__":
    pb = PyBreak()
    pb.main_loop()
