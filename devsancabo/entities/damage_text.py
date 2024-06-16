import pygame

from devsancabo.entities.base import Drawable
from devsancabo.graphics import Sprite, Graphics


class DamageText(Drawable):
    def __init__(self, text, x, y):
        font = pygame.font.Font('freesansbold.ttf', 24)
        text_surface = font.render(text, True, Graphics.WHITE)
        text_s = Sprite(text_surface)
        self.set_position(x, y)
        text_surface_rect = text_s.get_image().get_rect()
        super().__init__(text_s, x, y, text_surface_rect.width, text_surface_rect.height)
        self.__alpha = 255
        self.__lag = 60

    def update_state(self, lag):
        self.set_position(self.get_position()[0], self.get_position()[1] - 1)
        self.__lag = lag

    def render(self, percentage, graphics, sprite_sheet_box=None):
        self.__alpha = self.__alpha - (0.255 * self.__lag)
        self.set_position(self.get_position()[0], self.get_position()[1] - 1*(percentage / self.__lag))
        self.sprite.get_image().set_alpha(self.__alpha)
        super().render(percentage, graphics)

    def is_done(self):
        return False
