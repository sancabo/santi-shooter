import pygame

from devsancabo.entities.base import Drawable
from devsancabo.graphics import Graphics, Sprite


class Text(Drawable):

    def __init__(self, text: str, size: int, center: (int, int) = (0, 0), color: (int, int, int) = (255, 255, 255)):
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(text, True, color)
        self.__text = Sprite(text_surface)
        text_surface_rect = self.__text.get_image().get_rect()
        text_surface_rect.center = center
        super().__init__(self.__text, text_surface_rect.left, text_surface_rect.top,
                         text_surface_rect.width, text_surface_rect.height)
