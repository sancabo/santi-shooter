import pygame

from devsancabo.entities.projectile.projectile import Projectile
from devsancabo.graphics import Sprite


class Shot(Projectile):
    def __init__(self, time_to_live_ms: int = 10000):
        super().__init__(time_to_live_ms)
        self.__original__sprite_sheet = pygame.image.load("assets/fire-circles.png").convert_alpha()
        self.__scale_factor = 1
        self.__sprite_sheet = pygame.transform.scale_by(self.__original__sprite_sheet, self.__scale_factor)
        self.__sprite_size = (50, 50)
        self.__sprite_sheet_size = (8, 8)
        self.__position = (0, 0)
        self.__hit_box = (45, 45)
        self.set_image(Sprite(self.__sprite_sheet))
        self.set_dimensions((50, 50))

    def set_entity_position(self, coord):
        self.__position = coord
        self.set_position(self.__position[0], self.__position[1])

    def update_state(self, lag):
        deltas = self.calculate_movement_deltas(lag, 0)
        self.__position = (self.__position[0] + deltas[0], self.__position[1] + deltas[1])
        super().update_state(lag)

    def render(self, percentage, graphics, box=None):
        deltas = self.calculate_movement_deltas(0, percentage)
        self.__position = (self.__position[0] + deltas[0], self.__position[1] + deltas[1])
        self.set_position(self.__position[0], self.__position[1])
        sprite_sheet_total = self.__sprite_sheet_size[0]*self.__sprite_sheet_size[1]
        x, y = self.animation_cycle % 8, self.animation_cycle // self.__sprite_sheet_size[1]
        size = self.__sprite_size[0] * self.__scale_factor
        sprite_sheet_box = pygame.Rect(x, y * size, size, size)
        self.animation_cycle = (self.animation_cycle + 2) % sprite_sheet_total

        graphics.draw_entity(self.sprite, self.__position, sprite_sheet_box)

    def get_col_box(self) -> (int, int, int, int):
        _tuple = (self.__position[0],
                  self.__position[1],
                  self.__hit_box[0],
                  self.__hit_box[1])
        return _tuple

    def move_entity(self, x, y):
        self.__position = (self.__position[0] + x, self.__position[1] + y)