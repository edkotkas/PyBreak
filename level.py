import pygame
import random
import sys
import ast

from helpers import TextBox


def colour_generator():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


class Level:
    def __init__(self, stage=None):
        """
        Level manager.
        :return:
        """
        if stage is not None:
            self._stage = stage
        else:
            self._stage = 1

        self._stages = []
        self._map = []

        with open("stages.lvl") as level_file:
            for all_stages in level_file.read().strip(' \t\n\r').split('='):
                self._stages.append(all_stages)

        for current_map in self._stages[self._stage].split('-'):
            self._map.append(ast.literal_eval(current_map))

    def cleared(self):
        """
        Level finished manager.
        :return:
        """
        print len(self._map)
        if len(self._map) <= 1:
            if self._stage <= len(self._stages):
                self._stage += 1
                with open("stages.lvl") as level_file:
                    for all_stages in level_file.read().strip(' \t\n\r').split('='):
                        self._stages.append(all_stages)
                for current_map in self._stages[self._stage].split('-'):
                    self._map.append(ast.literal_eval(current_map))
            return True
        else:
            return False

    def map(self):
        """
        Returns a map of blocks.
        :return:
        """
        self.map_size = len(self._map)
        for b in self._map:
            yield b

    def hit(self, block):
        """
        Removes a hit block.
        :param block:
        :return:
        """
        self._map.remove(block)


class LevelEditor:
    def __init__(self):
        """
        Level designer.
        :return:
        """

        pygame.init()

        self.display = pygame.display.Info()

        self.window_width = 640
        self.window_height = 640

        self.grid_size = 40
        self.grid_x = self.window_width / self.grid_size
        self.grid_y = self.window_height / self.grid_size

        self.fps = 60

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        self.block_size = 3

        self.generated_colours = []
        for colour_x in range(15, self.grid_size):
            for colour_y in range(26, self.grid_size):
                self.generated_colours.append(colour_generator())

    def loop(self):
        allowed_slots = []
        current_block = None
        mouse_pos = (0, 0)

        block_colour_default = (255,) * 3

        place_block = True
        placed_blocks = []

        first_run = True
        colour_first_run = True

        length_increase_text = None
        length_decrease_text = None

        colour_selector = []

        save_button = None

        while True:
            self.screen.fill((10, 10, 10))

            for event in pygame.event.get():

                mouse_pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:
                        if place_block is True and current_block is not None:
                            placed_blocks.append(current_block)

                        if length_increase_text is not None and length_decrease_text is not None:
                            if length_decrease_text.collidepoint(mouse_pos):
                                if self.block_size > 1:
                                    self.block_size -= 1
                            if length_increase_text.collidepoint(mouse_pos):
                                if self.block_size < self.grid_size:
                                    self.block_size += 1

                            for index, colour in enumerate(colour_selector):
                                if colour.collidepoint(mouse_pos):
                                    block_colour_default = self.generated_colours[index]

                            if save_button.collidepoint(mouse_pos) \
                                    and save_button is not None and len(placed_blocks) > 0:
                                with open("stages.lvl", 'a+') as f:
                                    s = "-".join(str(i) for i in placed_blocks)
                                    f.write("=%s" % s)

                                with open("stages.lvl", 'r') as f:
                                    for i in f.read().split('='):
                                        for j in i.split('-'):
                                            print j

                    if event.button == 3:

                        for clicked_block in placed_blocks:
                            if pygame.Rect(clicked_block[1]).collidepoint(mouse_pos):
                                placed_blocks.remove(clicked_block)

            # grid for placing blocks
            for grid_x in range(self.grid_size):
                for grid_y in range(self.grid_size - 15):
                    pygame.draw.rect(self.screen, (100,) * 3, (
                        0 + self.grid_x * grid_x, 0 + self.grid_y * grid_y,
                        self.grid_x, self.grid_y
                    ), 1)

                    if first_run is True:
                        allowed_slots.append((
                            0 + self.grid_x * grid_x, 0 + self.grid_y * grid_y, self.grid_x, self.grid_y
                        ))
            first_run = False

            # display currently placed blocks
            if len(placed_blocks) > 0:
                for saved_blocks in placed_blocks:
                    pygame.draw.rect(self.screen, *saved_blocks)

            # block placing mechanics
            place_block = True
            current_block = None
            for x, y, xs, ys in allowed_slots:
                block = x, y, xs * self.block_size, ys
                block_colour = block_colour_default
                if pygame.Rect(x, y, xs, ys).collidepoint(mouse_pos):
                    current_block = block_colour, block

                    if x + xs * self.block_size > self.window_width or y > self.grid_y * 25:
                        block_colour = (255, 0, 0)
                        place_block = False

                    if len(placed_blocks) > 0:
                        for p_blocks in placed_blocks:
                            if pygame.Rect(p_blocks[1]).colliderect(current_block[1]):
                                block_colour = (255, 0, 0)
                                place_block = False

                    pygame.draw.rect(self.screen, block_colour, block)

            # bottom bar for selecting block options
            pygame.draw.rect(self.screen, (100, 50, 50), (
                0, self.grid_y * 26,
                self.grid_x * 40, self.grid_y * 14
            ))

            colour_counter = 0
            for colour_x in range(15, self.grid_size):
                for colour_y in range(26, self.grid_size):
                    colour_block = pygame.draw.rect(self.screen, self.generated_colours[colour_counter], (
                        0 + self.grid_x * colour_x, 0 + self.grid_y * colour_y,
                        self.grid_x, self.grid_y
                    ))
                    if colour_first_run is True:
                        colour_selector.append(colour_block)
                    colour_counter += 1
            colour_first_run = False

            # options for block size...
            pygame.draw.rect(self.screen, (15,) * 3, (
                0, self.grid_y * 26,
                self.grid_x * 15, self.grid_y * 14
            ))

            self.screen.blit(
                TextBox("Length :  " + str(self.block_size), 18, font="arial").make(),
                (self.grid_x, self.grid_y * 27)
            )

            length_increase_text = self.screen.blit(
                TextBox("+", 24, font="arial").make(), (self.grid_x * 10, self.grid_y * 26 + 10)
            )

            length_decrease_text = self.screen.blit(
                TextBox("-", 26, font="arial").make(), (self.grid_x * 8, self.grid_y * 26 + 10)
            )

            save_button = pygame.draw.rect(self.screen, (100,) * 3, (self.grid_x, self.grid_y * 30, 93, 23))
            self.screen.blit(
                TextBox("Save Stage", 18, font="arial").make(),
                (self.grid_x, self.grid_y * 30)
            )

            pygame.time.Clock().tick(self.fps)
            pygame.display.flip()


if __name__ == "__main__":
    editor = LevelEditor()
    editor.loop()
