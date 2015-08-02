

class MoveHelper:

    def __init__(self):
        self.LEFT = 0
        self.RIGHT = 1
        self.UP = 2
        self.DOWN = 3

    def opposite(self, direction):
        """
        Returns the opposite of the direction.
        :param direction:
        :return:
        """
        if direction == self.LEFT:
            return self.RIGHT
        if direction == self.RIGHT:
            return self.LEFT
        if direction == self.UP:
            return self.DOWN
        if direction == self.DOWN:
            return self.UP
