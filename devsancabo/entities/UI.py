import pygame

from devsancabo.graphics import Sprite, Drawable


class UserInterface(Drawable):

    def __init__(self):
        self.__hp_bar = pygame.Surface((500, 20))
        self.__hp_bar.fill((255, 0, 0))
        self.__percentage_filled = 1
        super().__init__(Sprite(self.__hp_bar), 20, 20, 500, 20)

    def drain_hp(self, percentage):
        self.__percentage_filled = self.__percentage_filled - percentage
        if self.__percentage_filled < 0:
            self.__percentage_filled = 0
        if self.__percentage_filled > 1:
            self.__percentage_filled = 1
        self.__hp_bar.fill((0, 0, 0), pygame.Rect(500 - 500*(1 - self.__percentage_filled), 0,
                                                  501*(1 - self.__percentage_filled), 20))
        self.set_image(Sprite(self.__hp_bar))

