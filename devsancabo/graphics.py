import pygame


class Graphics:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))

    def draw_entity(self, sprite, rectangle_entity, area_of_sprite=None):
        if area_of_sprite is not None:
            self.screen.blit(sprite.get_image(), rectangle_entity, area_of_sprite)
        else:
            self.screen.blit(sprite.get_image(), rectangle_entity)

    def print_screen(self):
        pygame.display.update()


class Sprite:
    def __init__(self, surface):
        self.__surface = surface

    def get_image(self):
        return self.__surface


