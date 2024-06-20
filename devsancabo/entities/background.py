import pygame

from devsancabo.graphics import Sprite, Graphics, Drawable


# todo: make background bigger
class Background(Drawable):

    def __init__(self):
        sprite_image = pygame.image.load("assets/background.jpg").convert_alpha()

        self.big_background = pygame.surface.Surface((5000.00, 5000.00))

        self.big_background.blit(sprite_image, (0, 0))
        self.big_background.blit(sprite_image, (0, 800))
        self.big_background.blit(sprite_image, (1195, 0))
        self.big_background.blit(sprite_image, (1195, 800))
        self.big_background.blit(sprite_image, (0, 1600))
        self.big_background.blit(sprite_image, (1195, 1600))
        self.big_background.blit(sprite_image, (2390, 0))
        self.big_background.blit(sprite_image, (2390, 800))
        self.big_background.blit(sprite_image, (2390, 1600))

        super().__init__(Sprite(self.big_background))

        font = pygame.font.Font('freesansbold.ttf', 42)
        text_surface = font.render("Move around with WASD", True, Graphics.WHITE)
        text_surface_2 = font.render("Exit with ESC. Pause with SPACE", True, Graphics.WHITE)
        text_surface_3 = font.render("sancabo@github", True, Graphics.WHITE)
        self.__text = Sprite(text_surface)
        self.__text_2 = Sprite(text_surface_2)
        self.__text_3 = Sprite(text_surface_3)
        self.__text_rect = self.__text.get_image().get_rect()
        self.__text_rect.center = (pygame.display.get_surface().get_width() // 2,
                                   pygame.display.get_surface().get_height() // 2 - 42 - 20)
        self.__text_rect_2 = self.__text_2.get_image().get_rect()
        self.__text_rect_2.center = (pygame.display.get_surface().get_width() // 2,
                                     pygame.display.get_surface().get_height() // 2)
        self.__text_rect_3 = self.__text_3.get_image().get_rect()
        self.__text_rect_3.center = (pygame.display.get_surface().get_width() // 2,
                                     (pygame.display.get_surface().get_height() // 2) + 42 + 20)

        self.set_position(0, 0)
        self.set_dimensions((5000, 5000))

    def render(self, percentage, graphics, camera=None, sprite_sheet_box=None):
        base = self.big_background.copy()
        base.blit(self.__text.get_image(), self.__text_rect)
        base.blit(self.__text_2.get_image(), self.__text_rect_2)
        base.blit(self.__text_3.get_image(), self.__text_rect_3)
        self.set_image(Sprite(base))
        super().render(percentage, graphics, camera, sprite_sheet_box)
