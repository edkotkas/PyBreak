from helpers import MoveHelper


class Item:

    def __init__(self, width=None, height=None, position=None, colour=None, step=None):
        """
        Item manager(ball, paddle, blocks, etc.).
        :return:
        """
        self._size = width, height
        self._position = position
        self._colour = colour
        self._step = step

        self.direction = MoveHelper()

    def size(self, width=None, height=None):
        """
        Size controller.
        :return:
        """
        if width is not None and height is not None:
            self._size = width, height
        else:
            return self._size

    def step(self, length=None):
        """
        Movement length.
        :param length:
        :return:
        """
        if length is not None:
            self._step = length
        else:
            return self._step

    def position(self, x=None, y=None):
        """
        Position controller.
        :return:
        """
        if x is not None and y is not None:
            self._position = (x, y)
        if x is not None:
            self._position = (x, self._position[1])
        if y is not None:
            self._position = (self._position[0], y)
        else:
            return self._position

    def colour(self, colour=None):
        """
        Colour controller.
        :return:
        """
        if colour is not None:
            self._colour = colour
        else:
            return self._colour

    def move(self, direction):
        """
        Moves the paddle position.
        :param direction:
        :return:
        """
        move_x, move_y = self.position()
        if direction == self.direction.LEFT:
            self.position(x=move_x - self.step())
        if direction == self.direction.RIGHT:
            self.position(x=move_x + self.step())
        if direction == self.direction.UP:
            self.position(y=move_y - self.step())
        if direction == self.direction.DOWN:
            self.position(y=move_y + self.step())

    def render(self):
        """
        Blittable object.
        :return:
        """
        return self.colour(), (self.position()[0], self.position()[1],
                               self.size()[0], self.size()[1])
