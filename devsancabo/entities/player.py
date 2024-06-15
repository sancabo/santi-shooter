import math

import pygame

from devsancabo.entities.base import Drawable, Collisionable
from devsancabo.graphics import Sprite

INFINITY_THRESHOLD = 999999

ONE_SEC = 1000


class Player(Drawable, Collisionable):

    def __init__(self, slippery_factor: int = INFINITY_THRESHOLD, top_speed: float = INFINITY_THRESHOLD, hp = 500):
        self.__sprite_sheet = pygame.image.load("assets/car_sprites.png").convert_alpha()

        # Used for Collisionable
        self.__player_box = pygame.Rect(100, 100, 150, 150)

        self.__orientation = 180
        super().__init__(Sprite(self.__sprite_sheet), 100, 100, 40, 40)

        self.__top_speed = top_speed
        self.__current_speed_x = 0
        self.__current_speed_y = 0
        self.__acceleration_x = 0
        self.__acceleration_y = 0
        self.__natural_friction = slippery_factor  # 999999 infinite

        self.__hit_points = hp
        self.__inv_toggle = True
        self.__invulnerable_ms_left = 0

    # To do, reduce 'col box', center on 'render box'
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
        self.__calculate_velocity_y(lag)

        self.__calculate_velocity_x(lag)

        return (self.__current_speed_x * float(lag / ONE_SEC + (lag * percentage) / ONE_SEC),
                self.__current_speed_y * float(lag / ONE_SEC + (lag * percentage) / ONE_SEC))

    def __calculate_velocity_y(self, lag):
        if self.__acceleration_y == 0:
            # if slippery is not infinite, gradually decrease speed
            if self.__natural_friction < INFINITY_THRESHOLD:
                self.__apply_slippery_instance_y(lag)
            else:
                self.__current_speed_y = 0
        else:
            self.__current_speed_y = self.__current_speed_y + float(self.__acceleration_y * lag / ONE_SEC)
        if self.__current_speed_y.__abs__() > self.__top_speed:
            if self.__current_speed_y > 0:
                self.__current_speed_y = self.__top_speed
            else:
                self.__current_speed_y = -self.__top_speed

    def __calculate_velocity_x(self, lag):
        if self.__acceleration_x == 0:
            # if slippery is not infinite, gradually decrease speed
            if self.__natural_friction < INFINITY_THRESHOLD:
                self.__apply_slippery_instance_x(lag)
            else:
                self.__current_speed_x = 0
        else:
            self.__current_speed_x = self.__current_speed_x + float(self.__acceleration_x * lag / ONE_SEC)
        if self.__current_speed_x.__abs__() > self.__top_speed:
            if self.__current_speed_x > 0:
                self.__current_speed_x = self.__top_speed
            else:
                self.__current_speed_x = -self.__top_speed

    def __apply_slippery_instance_x(self, lag):
        if self.__current_speed_x < 0:
            self.__current_speed_x = self.__current_speed_x + float(self.__natural_friction * lag / ONE_SEC)
            if self.__current_speed_x > 0:
                self.__current_speed_x = 0
        else:
            self.__current_speed_x = self.__current_speed_x - float(self.__natural_friction * lag / ONE_SEC)
            if self.__current_speed_x < 0:
                self.__current_speed_x = 0

    def __apply_slippery_instance_y(self, lag):
        if self.__current_speed_y < 0:
            self.__current_speed_y = self.__current_speed_y + float(self.__natural_friction * lag / ONE_SEC)
            if self.__current_speed_y > 0:
                self.__current_speed_y = 0
        else:
            self.__current_speed_y = self.__current_speed_y - float(self.__natural_friction * lag / ONE_SEC)
            if self.__current_speed_y < 0:
                self.__current_speed_y = 0

    # todo shadow under player
    def update_state(self, lag):
        deltas = self.__calculate_movement_deltas(lag, 0)
        self.__player_box = self.__player_box.move(deltas[0], deltas[1])
        # both speeds form a vector, according to its angle, adjust rotation
        # need to transform to degrees
        if self.__current_speed_y != 0 or self.__current_speed_x != 0:
            self.__orientation = math.atan2(self.__current_speed_y, self.__current_speed_x) * 57.2958
            if self.__orientation < 0:
                self.__orientation = 360 + self.__orientation
            self.__orientation = (self.__orientation + 92) % 360
        self.__update_state_invul(lag)

    def render(self, percentage, graphics, caca=None):
        deltas = self.__calculate_movement_deltas(0, percentage)
        self.__player_box = self.__player_box.move(deltas[0], deltas[1])

        # according to rotation, select correct sprite
        sprite_number = self.__orientation // 15
        x, y = sprite_number % 5, sprite_number // 5
        size = 830 // 5
        sprite_sheet_box = pygame.Rect(x * size, y * size, size, size)

        # delegate to drawable
        if self.__invulnerable_ms_left == 0:
            graphics.draw_entity(self.sprite, self.__player_box, sprite_sheet_box)
        else:
            if self.__inv_toggle:
                graphics.draw_entity(self.sprite, self.__player_box, sprite_sheet_box)
            self.__inv_toggle = not self.__inv_toggle


    def accelerate(self, x=None, y=None):
        if x is not None:
            self.__acceleration_x = x
        if y is not None:
            self.__acceleration_y = y

    def hurt(self, damage):
        self.__hit_points = self.__hit_points - damage
        self.__invulnerable_ms_left = 1000

    def is_vulnerable(self):
        return self.__invulnerable_ms_left == 0

    def __update_state_invul(self, lag):
        self.__invulnerable_ms_left = self.__invulnerable_ms_left - lag
        if self.__invulnerable_ms_left < 0:
            self.__invulnerable_ms_left = 0
