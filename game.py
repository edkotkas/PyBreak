import pygame
import random
import sys
import os

from items import Item
from levels import Level
from helpers import TextBox

os.environ['SDL_VIDEO_CENTERED'] = '1'

GRID_ENABLED = False


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

        # border helper
        self.window_border_top = 0
        self.window_border_left = 0
        self.window_border_right = self.window_width
        self.window_border_bottom = self.window_height

        self.grid_size = 40
        self.grid_x = self.window_width / self.grid_size
        self.grid_y = self.window_height / self.grid_size

        self.fps = 60

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.caption = pygame.display.set_caption("PyBreak - @edkotkas")

        # paddle settings
        self.paddle = Item()

        self.paddle_width = 9

        # change the single number up to half of the paddle width
        self.paddle_divert_range = self.grid_x * 3

        self.paddle.size(self.grid_x * self.paddle_width, self.grid_y)
        self.paddle.velocity(15)
        self.paddle.position(self.window_width/2 - self.paddle.size()[0]/2, self.grid_y * 34)
        self.paddle.colour((150, 75, 25))

        # ball settings
        self.ball = Item()
        self.ball.size(self.grid_x, self.grid_y)
        self.ball.velocity(4)
        self.ball.position(
            self.paddle.position()[0] + self.paddle.size()[0]/2 - self.ball.size()[0]/2,
            self.paddle.top - self.ball.size()[0]
        )
        self.ball.colour((255, 0, 100))

        # level settings
        self.level = Level(self.grid_x, self.grid_y)

        # text box
        self.text_box = TextBox

    def main_loop(self):
        """
        Main game loop.
        :return:
        """
        paddle_direction = None
        paddle_move_allowed = True
        ball_direction_y = self.ball.direction.UP
        ball_direction_x = random.choice([self.ball.direction.LEFT, self.ball.direction.RIGHT])

        game_started = False
        score = 0
        level = 1
        deaths = 0

        while True:
            self.screen.fill((10, 10, 10))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

                    if event.key == pygame.K_RIGHT:
                        paddle_direction = self.paddle.direction.RIGHT
                    if event.key == pygame.K_LEFT:
                        paddle_direction = self.paddle.direction.LEFT
                    if event.key == pygame.K_SPACE and game_started is False:
                        game_started = True

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

            # renders the paddle
            pygame.draw.rect(self.screen, *self.paddle.render())

            # paddle movement control
            if paddle_move_allowed is True:
                self.paddle.move(paddle_direction)

            # paddle boundary detection
            if self.paddle.left > self.window_border_left \
                    and paddle_direction is self.paddle.direction.LEFT \
                    or self.paddle.right < self.window_border_right \
                    and paddle_direction is self.paddle.direction.RIGHT:
                paddle_move_allowed = True
            else:
                paddle_move_allowed = False

            # move the ball with the paddle while game is not on
            if game_started is False:
                    self.ball.position(
                        self.paddle.position()[0] + self.paddle.size()[0]/2 - self.ball.size()[0]/2,
                        self.paddle.top - self.ball.size()[0]
                    )

            # ball movement control
            if game_started is True:
                self.ball.move(ball_direction_y)
                self.ball.move(ball_direction_x)

            # ball/boundary collision control
            # left / right of border
            if self.ball.left <= self.window_border_left:
                ball_direction_x = self.ball.direction.RIGHT
            if self.ball.right >= self.window_border_right:
                ball_direction_x = self.ball.direction.LEFT
            if self.ball.top <= self.window_border_top:
                ball_direction_y = self.ball.direction.DOWN
            # bottom of border
            if self.ball.bottom >= self.window_border_bottom:
                deaths += 1
                game_started = False

            # ball/paddle collision control
            if self.ball.bottom + self.ball.velocity()/2 >= self.paddle.top and self.ball.top < self.paddle.bottom \
                    and ball_direction_y == self.ball.direction.DOWN:

                if self.ball.left >= self.paddle.left and self.ball.right <= self.paddle.right:
                    ball_direction_y = self.ball.direction.opposite(ball_direction_y)

                if self.ball.left >= self.paddle.left \
                        and self.ball.right <= self.paddle.left + self.paddle_divert_range \
                        and ball_direction_x == self.ball.direction.RIGHT \
                        or self.ball.right <= self.paddle.right \
                        and self.ball.left >= self.paddle.right - self.paddle_divert_range \
                        and ball_direction_x == self.ball.direction.LEFT:
                    ball_direction_x = self.ball.direction.opposite(ball_direction_x)

            # ball/block collision control
            for block in self.level.map():

                if self.ball.top >= block.top \
                        and self.ball.bottom <= block.bottom \
                        and self.ball.left - self.ball.velocity() <= block.right < self.ball.right:
                    ball_direction_x = self.ball.direction.opposite(ball_direction_x)
                    self.level.hit(block)

                    score += 1

                    if score % 4 == 0 and level != 5:
                        level += 1
                        self.ball.velocity(self.ball.velocity() + 2)

                if self.ball.top >= block.top \
                        and self.ball.bottom <= block.bottom \
                        and self.ball.right + self.ball.velocity() >= block.left > self.ball.left:
                    ball_direction_x = self.ball.direction.opposite(ball_direction_x)
                    self.level.hit(block)

                    score += 1

                    if score % 4 == 0 and level != 5:
                        level += 1
                        self.ball.velocity(self.ball.velocity() + 2)

                # bottom of block, top of ball
                if self.ball.right <= block.right \
                        and self.ball.left >= block.left \
                        and self.ball.top - self.ball.velocity() <= block.bottom < self.ball.bottom:
                    ball_direction_y = self.ball.direction.opposite(ball_direction_y)
                    self.level.hit(block)

                    score += 1

                    if score % 4 == 0 and level != 5:
                        level += 1
                        self.ball.velocity(self.ball.velocity() + 2)

                # top of block, bottom of ball
                if self.ball.right <= block.right \
                        and self.ball.left >= block.left \
                        and self.ball.bottom + self.ball.velocity() >= block.top > self.ball.top:
                    ball_direction_y = self.ball.direction.opposite(ball_direction_y)
                    self.level.hit(block)

                    score += 1

                    if score % 4 == 0 and level != 5:
                        level += 1
                        self.ball.velocity(self.ball.velocity() + 1)

            # render blocks
            for render_block in self.level.map():
                pygame.draw.rect(self.screen, *render_block.render())

            # renders the ball
            pygame.draw.rect(self.screen, *self.ball.render())

            # renders the score text
            level_text = self.text_box("Level: " + str(level), 21)
            self.screen.blit(level_text.make(), (self.grid_x * 1, self.grid_y * 38))

            stage_text = self.text_box("Stage: " + str(0), 21)
            self.screen.blit(stage_text.make(), (self.grid_x * 10, self.grid_y * 38))

            score_text = self.text_box("Score: " + str(score), 21)
            self.screen.blit(score_text.make(), (self.grid_x * 20, self.grid_y * 38))

            death_text = self.text_box("Deaths: " + str(deaths), 21)
            self.screen.blit(death_text.make(), (self.grid_x * 30, self.grid_y * 38))

            pygame.display.flip()

if __name__ == "__main__":
    pb = PyBreak()
    pb.main_loop()
