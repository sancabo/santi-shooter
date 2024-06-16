import math

import pygame

from devsancabo.entities.base import Drawable, Collisionable
from devsancabo.graphics import Sprite

INFINITY_THRESHOLD = 999999

ONE_SEC = 1000


class Enemy(Drawable, Collisionable):

    def __init__(self, top_speed: float = INFINITY_THRESHOLD, hp = 500):
        self.__original__sprite_sheet = pygame.image.load("assets/fire-circles.png").convert_alpha()
        shadow = pygame.image.load("assets/glow-2.png").convert_alpha()
        self.__scale_factor = 2
        self.__sprite_size = (50, 50)
        self.__sprite_sheet_size = (8, 8)

        self.__sprite_sheet = pygame.transform.scale_by(self.__original__sprite_sheet, self.__scale_factor)
        shadow = pygame.transform.scale_by(shadow, self.__scale_factor*2)
        self.__shadow = Sprite(shadow)

        # Used for Collisionable
        self.__player_box = pygame.Rect(100, 100, 50*self.__scale_factor, 50*self.__scale_factor)
        self.__shadow_box = pygame.Rect(100, 100, 50*self.__scale_factor*2, 50*self.__scale_factor*2)

        self.__animation_cycle = 0
        super().__init__(Sprite(self.__sprite_sheet), 100, 100, 50*self.__scale_factor, 50*self.__scale_factor)

        self.__top_speed = top_speed
        self.__current_speed_x = 0
        self.__current_speed_y = 0
        self.__acceleration_x = 0
        self.__acceleration_y = 0

    def set_speed_vector(self, direction: (int, int), modulus: float):
        hypotenuse = math.hypot(direction[0], direction[1])
        ratio = modulus / hypotenuse
        self.__current_speed_x = direction[0] * ratio
        self.__current_speed_y = direction[1] * ratio

    def get_col_box(self) -> (int, int, int, int):
        _tuple = (self.__player_box.left,
                  self.__player_box.top,
                  self.__player_box.width,
                  self.__player_box.height)
        return _tuple

    def move_col_box(self, x, y):
        self.__player_box = self.__player_box.move(x, y)

    def relocate_col_box(self, x, y):
        self.__player_box = pygame.Rect(x, y, self.__player_box.width, self.__player_box.height)

    def __calculate_movement_deltas(self, lag, percentage):
        return (self.__current_speed_x * float(lag / ONE_SEC + (lag * percentage) / ONE_SEC),
                self.__current_speed_y * float(lag / ONE_SEC + (lag * percentage) / ONE_SEC))

    def update_state(self, lag):
        deltas = self.__calculate_movement_deltas(lag, 0)
        self.__player_box = self.__player_box.move(deltas[0], deltas[1])
        # both speeds form a vector, according to its angle, adjust rotation
        # need to transform to degrees

    def render(self, percentage, graphics, caca=None):
        deltas = self.__calculate_movement_deltas(0, percentage)
        self.__player_box = self.__player_box.move(deltas[0], deltas[1])
        sprite_sheet_total = self.__sprite_sheet_size[0]*self.__sprite_sheet_size[1]
        # according to rotation, select correct sprite
        x, y = self.__animation_cycle % 8, self.__animation_cycle//self.__sprite_sheet_size[1]
        size = self.__sprite_size[0] * self.__scale_factor
        sprite_sheet_box = pygame.Rect(x, y * size, size, size)
        draw = self.sprite
        self.__animation_cycle = (self.__animation_cycle + 2) % sprite_sheet_total

        self.__shadow_box.center = (self.__player_box.center[0], self.__player_box.center[1] + 20)

        graphics.draw_entity(self.__shadow, self.__shadow_box)
        # delegate to drawable
        graphics.draw_entity(draw, self.__player_box, sprite_sheet_box)

    def accelerate(self, x=None, y=None):
        # it skips acceleration
        if x is not None:
            self.__current_speed_x = x
        if y is not None:
            self.__current_speed_y = y

    def is_done(self):
        return False
