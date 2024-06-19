import pygame

from devsancabo.graphics import Sprite, Graphics, Drawable


class Background(Drawable):

    def __init__(self):
        sprite_image = pygame.image.load("assets/background.jpg").convert_alpha()

        big_background = pygame.surface.Surface((5000.00, 5000.00))

        big_background.blit(sprite_image, (0, 0))
        big_background.blit(sprite_image, (0, 800))
        big_background.blit(sprite_image, (1195, 0))
        big_background.blit(sprite_image, (1195, 800))
        big_background.blit(sprite_image, (0, 1600))
        big_background.blit(sprite_image, (1195, 1600))
        big_background.blit(sprite_image, (2390, 0))
        big_background.blit(sprite_image, (2390, 800))
        big_background.blit(sprite_image, (2390, 1600))

        super().__init__(Sprite(big_background))

        font = pygame.font.Font('freesansbold.ttf', 42)
        text_surface = font.render("Move around with WASD", True, Graphics.WHITE)
        text_surface_2 = font.render("Exit with ESC. Pause with SPACE", True, Graphics.WHITE)
        text_surface_3 = font.render("sancabo@github", True, Graphics.WHITE)
        self.__text = Sprite(text_surface)
        self.__text_2 = Sprite(text_surface_2)
        self.__text_3 = Sprite(text_surface_3)
        text_surface_rect = self.__text.get_image().get_rect()
        text_surface_rect.center = (pygame.display.get_surface().get_width() // 2,
                                    pygame.display.get_surface().get_height() // 2 - 42 - 20)
        text_surface_rect_2 = self.__text_2.get_image().get_rect()
        text_surface_rect_2.center = (pygame.display.get_surface().get_width() // 2,
                                      pygame.display.get_surface().get_height() // 2)
        text_surface_rect_3 = self.__text_3.get_image().get_rect()
        text_surface_rect_3.center = (pygame.display.get_surface().get_width() // 2,
                                      (pygame.display.get_surface().get_height() // 2) + 42 + 20)
        self.__text_rect = text_surface_rect
        self.__text_rect_2 = text_surface_rect_2
        self.__text_rect_3 = text_surface_rect_3

    def render(self, percentage, graphics, sprite_sheet_box=None):
        graphics.draw_entity(self.sprite, (0, 0))
        graphics.draw_entity(self.__text, self.__text_rect)
        graphics.draw_entity(self.__text_2, self.__text_rect_2)
        graphics.draw_entity(self.__text_3, self.__text_rect_3)
