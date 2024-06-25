
from devsancabo.entities.base import Collisionable
from devsancabo.graphics import Drawable


class Bounds(Drawable, Collisionable):

    def move_col_box(self, x, y):
        super().__position = (super().__position[0] + x, super().__position[1] + y)

    def get_col_box(self) -> (int, int, int, int):
        _tuple = (super().get_position()[0],
                  super().get_position()[1],
                  super().get_dimensions()[0],
                  super().get_dimensions()[1])
        return _tuple

    def __init__(self, x, y, w, h, sprite=None):
        super().__init__(sprite, x, y, w, h)

    def render(self, percentage, graphics, camera=None, sprite_sheet_box=None):
        # It's invisible
        pass
