import pygame

from devsancabo.entities.base import Drawable
from devsancabo.graphics import Sprite, Graphics


class Background(Drawable):

    def __init__(self):
        sprite = pygame.image.load("assets/background.jpg").convert_alpha()
        # 1195 * 800
        uptra_big = pygame.surface.Surface((5000.00,5000.00))
        uptra_big.blit(sprite, (0, 0))
        uptra_big.blit(sprite, (800, 0))
        uptra_big.blit(sprite, (0, 1195))
        uptra_big.blit(sprite, (800, 1195))
        super().__init__(Sprite(uptra_big))
        font = pygame.font.Font('freesansbold.ttf', 42)
        text_surface = font.render("Move around with WASD", True, Graphics.WHITE, Graphics.BLACK)
        self.__text = Sprite(text_surface)
        text_surface_rect = self.__text.get_image().get_rect()
        text_surface_rect.center = (1280 // 2, 720 // 2)
        self.__text_rect = text_surface_rect

    def render(self, percentage, graphics):
        graphics.draw_entity(self.sprite, (0, 0))
        graphics.draw_entity(self.__text, self.__text_rect)
