import pygame

from devsancabo.entities.base import Drawable
from devsancabo.graphics import Sprite, Graphics


class Background(Drawable):

    def __init__(self):
        sprite = pygame.image.load("assets/background.jpg").convert_alpha()
        # 1195 * 800
        big_background = pygame.surface.Surface((5000.00, 5000.00))
        big_background.blit(sprite, (0, 0))
        big_background.blit(sprite, (800, 0))
        big_background.blit(sprite, (0, 1195))
        big_background.blit(sprite, (800, 1195))
        super().__init__(Sprite(big_background))
        font = pygame.font.Font('freesansbold.ttf', 42)
        text_surface = font.render("Move around with WASD", True, Graphics.WHITE)
        text_surface_2 = font.render("Exit with ESC", True, Graphics.WHITE)
        self.__text = Sprite(text_surface)
        self.__text_2 = Sprite(text_surface_2)
        text_surface_rect = self.__text.get_image().get_rect()
        text_surface_rect.center = (1280 // 2, 720 // 2 - 21 - 10)
        text_surface_rect_2 = self.__text_2.get_image().get_rect()
        text_surface_rect_2.center = (1280 // 2, (720 // 2) + 21 + 10)
        self.__text_rect = text_surface_rect
        self.__text_rect_2 = text_surface_rect_2

    def render(self, percentage, graphics, sprite_sheet_box=None):
        graphics.draw_entity(self.sprite, (0, 0))
        graphics.draw_entity(self.__text, self.__text_rect)
        graphics.draw_entity(self.__text_2, self.__text_rect_2)
