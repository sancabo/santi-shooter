import math

import pygame

from devsancabo.entities.base import GameEntity, Collisionable
from devsancabo.entities.camera import Camera
from devsancabo.graphics import Sprite, Drawable

ONE_SEC = 1000


class Shot(GameEntity, Collisionable):

    def __init__(self, position: tuple[int, int], time_to_live_ms: int = 10000):
        super().__init__("shot-{0}".format(self.__hash__()), position)
        self.__hit_box = (45, 45)
        self.__elapsed = 0
        self.__ttl = time_to_live_ms
        self.__current_speed_x = 0
        self.__current_speed_y = 0

        # encapsulate in Sprite()
        self.__original__sprite_sheet = pygame.image.load("assets/fire-circles.png").convert_alpha()
        self.__scale_factor = 1
        self.__sprite_sheet = pygame.transform.scale_by(self.__original__sprite_sheet, self.__scale_factor)
        self.__sprite_size = (50 * self.__scale_factor, 50 * self.__scale_factor)
        self.__sprite_sheet_matrix_size = (8, 8)
        self.__selected_sprite_n = 0
        drawable = Drawable(Sprite(pygame.Surface((1, 1))),
                            self.get_entity_position()[0],
                            self.get_entity_position()[1],
                            self.__sprite_size[0], self.__sprite_size[1])
        self.set_drawable(drawable)

    def update_state(self, lag):
        self.__elapsed = self.__elapsed + lag
        # print("update_state shot. elapsed = {0}".format(self.__elapsed))
        deltas = self.calculate_movement_deltas(lag, 0)
        self.move_entity(deltas)

    def render(self, percentage, graphics, camera: Camera, sprite_sheet_box=None):
        deltas = self.calculate_movement_deltas(0, percentage)
        self.move_entity(deltas)
        selected_sprite = self.select_sprite()
        self.get_drawable().set_image(Sprite(selected_sprite))
        self.get_drawable().set_position(self.get_entity_position()[0], self.get_entity_position()[1])
        self.get_drawable().render(percentage, graphics, camera, percentage)

    def is_done(self) -> bool:
        # print("is done = {0}".format(self.__elapsed > self.__ttl))
        return self.__elapsed > self.__ttl

    def select_sprite(self):
        new_surface = pygame.Surface(self.__sprite_size, pygame.SRCALPHA)
        n, m = (self.__selected_sprite_n % self.__sprite_sheet_matrix_size[0],
                self.__selected_sprite_n // self.__sprite_sheet_matrix_size[1])
        size = self.get_drawable().get_dimensions()
        sprite_sheet_box = pygame.Rect(n * size[0], m * size[1], size[0], size[1])
        new_surface.blit(self.__sprite_sheet, (0, 0), sprite_sheet_box)

        print("render sprite {0} - ({1}, {2}) - {3}".format(self.__selected_sprite_n, n, m, sprite_sheet_box))

        self.__selected_sprite_n = ((self.__selected_sprite_n + 1) %
                                    ((self.__sprite_sheet_matrix_size[0] * self.__sprite_sheet_matrix_size[1]) - 3))
        return new_surface

    def get_col_box(self) -> (int, int, int, int):
        col_box = pygame.Rect(0, 0, self.__hit_box[0], self.__hit_box[1])
        col_box.center = pygame.Rect(self.get_drawable().get_position()[0],
                                     self.get_drawable().get_position()[1],
                                     self.get_drawable().get_dimensions()[0],
                                     self.get_drawable().get_dimensions()[1]).center
        return col_box.left, col_box.top, col_box.width, col_box.height

    def move_col_box(self, x, y):
        print("Cannot move hit box of entity {0}".format(self.get_id()))

    def set_speed_vector(self, direction: (int, int), modulus: float):
        hypotenuse = math.hypot(direction[0], direction[1])
        ratio = modulus / hypotenuse
        self.__current_speed_x = direction[0] * ratio
        self.__current_speed_y = direction[1] * ratio

    def calculate_movement_deltas(self, lag, percentage):
        return (self.__current_speed_x * float(lag / ONE_SEC + (lag * percentage) / ONE_SEC),
                self.__current_speed_y * float(lag / ONE_SEC + (lag * percentage) / ONE_SEC))
