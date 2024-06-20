import pygame

from devsancabo.entities.base import GameEntity


class Camera(GameEntity):
    def __init__(self, rect: tuple[int, int, int, int], identifier: str = None):
        if identifier is None:
            super().__init__("Camera-{0}".format(self.__hash__()))
        else:
            super().__init__(identifier)

        self.__bounds = pygame.Rect(rect[0], rect[1], rect[2], rect[3])

    def is_touching(self, x2, y2, w2, h2) -> bool:
        return self.__bounds.colliderect((x2, y2, w2, h2))
        # print("is touching?")
        # x1, y1, w1, h1 = self.__bounds.left, self.__bounds.top, self.__bounds.width, self.__bounds.height
        # if disjointed by x or disjointed by y -> are not touching
        # return not (x1 + w1 < x2 or x1 > x2 + w2 or y1 > y2 + h2 or y1 + h1 < y2)


pass
