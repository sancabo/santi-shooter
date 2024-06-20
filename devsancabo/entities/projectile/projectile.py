import math

import pygame

from devsancabo.entities.base import Collisionable
from devsancabo.graphics import Sprite, Drawable

INFINITY_THRESHOLD = 999999

ONE_SEC = 1000


class Projectile(Drawable, Collisionable):

    def __init__(self, time_to_live_ms: int = 10000):
        self.__time_alive = 0
        self.__original__sprite_sheet = pygame.image.load("assets/fire-circles.png").convert_alpha()
        shadow = pygame.image.load("assets/glow-2.png").convert_alpha()
        self.__scale_factor = 2
        self.__sprite_size = (50, 50)
        self.__sprite_sheet_size = (8, 8)
        self.__ttl = time_to_live_ms

        self.__sprite_sheet = pygame.transform.scale_by(self.__original__sprite_sheet, self.__scale_factor)
        shadow = pygame.transform.scale_by(shadow, self.__scale_factor * 2)
        self.__shadow = Sprite(shadow)

        self.__player_box = pygame.Rect(100, 100, 50 * self.__scale_factor, 50 * self.__scale_factor)
        self.__shadow_box = pygame.Rect(100, 100, 50 * self.__scale_factor * 2, 50 * self.__scale_factor * 2)

        self.animation_cycle = 0
        super().__init__(Sprite(self.__sprite_sheet), 100, 100, 50 * self.__scale_factor, 50 * self.__scale_factor)
        self.set_dimensions((self.__shadow_box.width, self.__shadow_box.height))

        self.__current_speed_x = 0
        self.__current_speed_y = 0

        self.__frame = pygame.Surface((self.__shadow_box.width, self.__shadow_box.height), pygame.SRCALPHA)

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

    def calculate_movement_deltas(self, lag, percentage):
        return (self.__current_speed_x * float(lag / ONE_SEC + (lag * percentage) / ONE_SEC),
                self.__current_speed_y * float(lag / ONE_SEC + (lag * percentage) / ONE_SEC))

    def update_state(self, lag):
        self.__time_alive = self.__time_alive + lag
        deltas = self.calculate_movement_deltas(lag, 0)
        self.__player_box = self.__player_box.move(deltas[0], deltas[1])
        # both speeds form a vector, according to its angle, adjust rotation
        # need to transform to degrees

    def render_skip(self, camera, percentage, graphics, caca=None):
        super().render(percentage, graphics, camera, caca)

    def render(self, percentage, graphics, camera=None, sprite_sheet_box=None):
        # do something with camera
        # encapsulate drawing to drawable
        deltas = self.calculate_movement_deltas(0, percentage)
        self.__player_box = self.__player_box.move(deltas[0], deltas[1])
        sprite_sheet_total = self.__sprite_sheet_size[0] * self.__sprite_sheet_size[1]
        # according to rotation, select correct sprite
        x, y = self.animation_cycle % 8, self.animation_cycle // self.__sprite_sheet_size[1]
        size = self.__sprite_size[0] * self.__scale_factor
        sprite_sheet_box = pygame.Rect(x, y * size, size, size)
        self.animation_cycle = (self.animation_cycle + 2) % sprite_sheet_total
        self.__shadow_box.center = self.__player_box.center

        frame = self.__frame.copy()
        frame.blit(self.__sprite_sheet,
                   (self.__player_box.left - self.__shadow_box.left, self.__player_box.top - self.__shadow_box.top),
                   sprite_sheet_box)
        frame.blit(self.__shadow.get_image(), (0, 0))

        self.set_image(Sprite(frame))
        self.set_position(self.__shadow_box.left, self.__shadow_box.top)
        super().render(percentage, graphics, camera)

    def is_done(self):
        return self.__time_alive > self.__ttl
