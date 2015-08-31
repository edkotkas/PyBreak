from helpers import MoveHelper


class Item:

    def __init__(self, width=1, height=1, position=(0, 0), colour=(0, 0, 0), step=1):
        """
        Item manager(ball, paddle, blocks, etc.).
        :return:
        """
        self._size = width, height
        self._position = position
        self._colour = colour
        self._velocity = step

        self.left = self._position[0]
        self.top = self._position[1]
        self.right = self._position[0] + self._size[0]
        self.bottom = self._position[1] + self._size[1]
        self.middle = self.right/2

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

        self._update()

    def velocity(self, speed=None):
        """
        Movement length.
        :param speed:
        :return:
        """
        if speed is not None:
            self._velocity = speed
        else:
            return self._velocity

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

        self._update()

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
            self.position(x=move_x - self.velocity())
        if direction == self.direction.RIGHT:
            self.position(x=move_x + self.velocity())
        if direction == self.direction.UP:
            self.position(y=move_y - self.velocity())
        if direction == self.direction.DOWN:
            self.position(y=move_y + self.velocity())

        self._update()

    def render(self):
        """
        Blittable object.
        :return:
        """
        return self.colour(), (self.position()[0], self.position()[1],
                               self.size()[0], self.size()[1])

    def _update(self):
        self.left = self._position[0]
        self.top = self._position[1]
        self.right = self._position[0] + self._size[0]
        self.bottom = self._position[1] + self._size[1]
