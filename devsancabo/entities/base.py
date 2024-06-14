from abc import abstractmethod

import pygame

from devsancabo.graphics import Sprite


class Drawable:

    def __init__(self, sprite: Sprite, x=0, y=0, width=0, height=0):
        self.sprite = sprite
        self.__position = (x, y)
        self.__dimensions = (width, height)

    def set_image(self, sprite: Sprite):
        self.sprite = sprite

    def get_position(self) -> (int, int):
        return self.__position

    def get_dimensions(self) -> (int, int):
        return self.__dimensions

    def render(self, percentage, graphics, sprite_sheet_box=None):
        graphics.draw_entity(
            self.sprite, pygame.Rect(self.__position[0],
                                     self.__position[1],
                                     self.__dimensions[0],
                                     self.__dimensions[1]),
            sprite_sheet_box)


class Collisionable:
    @abstractmethod
    def get_col_box(self) -> (int, int, int, int):
        pass

    @abstractmethod
    def move_col_box(self, x, y):
        pass

    def is_touching(self, other) -> bool:
        # print("is touching?")
        x1, y1, w1, h1 = self.get_col_box()
        x2, y2, w2, h2 = other.get_col_box()
        # if disjointed by x or disjointed by y -> are not touching
        return not (x1 + w1 < x2 or x1 > x2 + w2 or y1 > y2 + h2 or y1 + h1 < y2)

    def is_inside(self, other):
        x1, y1, w1, h1 = self.get_col_box()
        x2, y2, w2, h2 = other.get_col_box()

        return x2 < x1 and x1 + w1 < x2 + w2 and y2 < y1 and y1 + h1 < y2 + h2


class Moveable:
    # Moveable.apply_accel(accel, residual_lag)
    #   accel how much coord/second I want to modify the speed each second
    #   residual_lag value to add to #update_lag
    # Moveable.set_top_speed(top_speed)
    # Moveable.set_slippery_scale(slippery_scale)
    # Moveable(update_lag, slippery_scale = 1, top_speed = 1)
    #   update_lag used to scale speed and acceleration for calculation
    #   maximum coord/millisecond this entity can move
    #   slippery_scale how much of it's speed it loses each at stop, and each update
    # todo implement "Enemy" type. Use moveable to share behaviour with "Player"
    pass

# todo implement attach method, to allow composition of game entities. They move and render together