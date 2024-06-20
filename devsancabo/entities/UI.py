import pygame

from devsancabo.entities.camera import Camera
from devsancabo.graphics import Sprite, Drawable


class UserInterface(Drawable):

    def __init__(self):
        self.__width = pygame.display.get_window_size()[0]/4
        self.__height = 40
        self.__hp_bar = pygame.Surface((self.__width, self.__height))
        self.__hp_bar.fill((255, 0, 0))
        self.__percentage_filled = 1
        super().__init__(Sprite(self.__hp_bar), self.__height*2,
                         self.__height*2,
                         self.__width, self.__height)

    def drain_hp(self, percentage):
        self.__percentage_filled = self.__percentage_filled - percentage
        if self.__percentage_filled < 0:
            self.__percentage_filled = 0
        if self.__percentage_filled > 1:
            self.__percentage_filled = 1
        self.__hp_bar.fill((0, 0, 0), pygame.Rect(self.__width - self.__width*(1 - self.__percentage_filled), 0,
                                                  self.__width*(1 - self.__percentage_filled), self.__height))
        self.set_image(Sprite(self.__hp_bar))

    def render(self, percentage, graphics, camera: Camera = None, sprite_sheet_box=None):
        super().render(percentage, graphics)

