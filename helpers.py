import pygame

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

class TextBox:

    def __init__(self, string="TextBox", size=14, colour=(250,)*3, font="monospace"):
        """
        PyGame text renderer.
        :param string: text to be shown
        :param size: font size
        :param colour: font colour
        :param font: font family
        :return:
        """
        self._string = string
        self._size = size
        self._colour = colour
        self._font = font

    def string(self, s=None):
        """
        String controller.
        :return: string
        """
        if s is not None:
            self._string = s
        else:
            return self._string

    def size(self, s=None):
        """
        Size controller.
        :return:
        """
        if s is not None:
            self._size = s
        else:
            return self._size

    def colour(self, c=None):
        """
        Colour controller.
        :return:
        """
        if c is not None:
            self._colour = c
        else:
            return self._colour

    def font(self, f=None):
        """
        Colour controller.
        :return:
        """
        if f is not None:
            self._font = f
        else:
            return self._font

    def make(self):
        """
        Creates text for blit.
        :return:
        """
        return pygame.font.SysFont(self._font, self._size).render(self._string, 1, self._colour)