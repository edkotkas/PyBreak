import random
from items import Item


class Level:

    def __init__(self, grid_x, grid_y, stage=None):
        """
        Level manager.
        :return:
        """

        self.stage = stage

        self.grid_x = grid_x
        self.grid_y = grid_y

        self.blocks = Item()

        # temporary map layout
        # distance, distance, line - amount
        self.tiles = [
            [
                (1, 10, 0),
            ] * 4,
            [
                (1, 4, 1),
            ] * 10,
            [
                (3, 10, 2),
            ] * 2,
            [
                (3, 4, 3),
            ] * 4,
            [
                (3, 4, 4),
            ] * 4,
            [
                (3, 4, 5),
            ] * 4,
            [
                (9, 4, 6),
            ] * 2,
            [
                (9, 4, 7),
            ] * 2,
            [
                (9, 4, 8),
            ] * 2,
            [
                (9, 4, 9),
            ] * 2,
            [
                (9, 4, 10),
            ] * 2,
            [
                (2, 8, 11),
            ] * 3,
            [
                (9, 4, 12),
            ] * 2,
            [
                (9, 4, 13),
            ] * 2,
            [
                (9, 4, 14),
            ] * 2,
            [
                (9, 4, 15),
            ] * 2,
            [
                (9, 4, 16),
            ] * 2,
            [
                (3, 10, 17),
            ] * 2,
            [
                (1, 4, 18),
            ] * 10,
            [
                (1, 10, 19),
            ] * 4,
        ]

        # test block
        self._map = []

        for line in self.tiles:
            for x, (s, w, y) in enumerate(line):
                self.block = Item()
                self.block.size(w * self.grid_x, 1 * self.grid_y)
                self.block.position(x * self.grid_x * w * s, y * self.grid_y)
                self.block.colour(self.colour())

                self._map.append(self.block)

    def map(self):
        """
        Returns a map of blocks.
        :return:
        """
        for blocks in self._map:
            yield blocks

    def hit(self, block):
        """
        Removes a hit block.
        :param block:
        :return:
        """
        self._map.remove(block)

    def colour(self):
        return random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)

