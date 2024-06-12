

from devsancabo.entities.base import Drawable, Collisionable


class Bounds(Drawable, Collisionable):

    def get_box(self) -> (int, int, int, int):
        thetuple = (super().get_position()[0],
                super().get_position()[1],
                super().get_dimensions()[0],
                super().get_dimensions()[1])
        # print("Get background box! ", thetuple)
        return thetuple

    def __init__(self, x, y, w, h, sprite=None):
        super().__init__(sprite, x, y, w, h)

    def render(self, percentage, graphics):
        # It's invisible
        pass