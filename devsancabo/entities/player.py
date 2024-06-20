import math

import pygame

from devsancabo.audio import Audio
from devsancabo.entities.base import Collisionable
from devsancabo.graphics import Sprite, Drawable

INFINITY_THRESHOLD = 999999

ONE_SEC = 1000


class Player(Drawable, Collisionable):

    def __init__(self, audio: Audio, slippery_factor: int = INFINITY_THRESHOLD, top_speed: float = INFINITY_THRESHOLD,
                 hp=500):
        self.__audio = audio
        self.__is_playing = False
        self.__sprite_sheet = pygame.image.load("assets/car_sprites.png").convert_alpha()
        self.__state = "alive"

        # Used for Collisionable
        self.__player_box = pygame.Rect(100, 100, 150, 150)
        self.__engine_sound = self.__audio.make_sound("assets/engine.wav")

        self.__orientation: float = 180.00
        super().__init__(Sprite(self.__sprite_sheet), 100, 100, 40, 40)

        self.__top_speed = top_speed
        self.__current_speed_x = 0
        self.__current_speed_y = 0
        self.__acceleration_x = 0
        self.__acceleration_y = 0
        self.__natural_friction = slippery_factor  # 999999 infinite

        self.__hit_points = hp
        self.__max_hit_points = hp
        self.__inv_toggle = True
        self.__invulnerable_ms_left = 0
        self.__collision_enabled = True

        self.__sprite_sheet_dead = [pygame.image.load("assets/fire-frames/fire1_ 01.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 02.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 03.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 04.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 05.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 06.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 07.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 08.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 09.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 10.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 11.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 12.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 13.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 14.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 15.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 16.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 17.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 18.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 19.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 20.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 21.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 22.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 23.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 24.png").convert_alpha(),
                                    pygame.image.load("assets/fire-frames/fire1_ 25.png").convert_alpha()]
        self.__death_sprite_number = 0

        # To do, reduce 'col box', center on 'render box'

    def get_col_box(self) -> (int, int, int, int):
        col_box = pygame.Rect(self.__player_box.left,
                              self.__player_box.top,
                              self.__player_box.width * 0.5,
                              self.__player_box.height * 0.5)
        col_box.center = self.__player_box.center
        _tuple = (col_box.left,
                  col_box.top,
                  col_box.width,
                  col_box.height)
        return _tuple

    def move_col_box(self, x, y):
        self.__player_box = self.__player_box.move(x, y)

    def relocate_col_box(self, x, y):
        self.__player_box = pygame.Rect(x, y, self.__player_box.width, self.__player_box.height)

    def relocate_in_bounds(self, bounds):
        px, py, pw, ph = self.get_col_box()
        bx, by, bw, bh = bounds.get_col_box()
        if px < bx:
            self.move_col_box(bx - px + 1, 0)
        if px + pw > bx + bw:
            self.move_col_box(-px - pw + bx + bw - 1, 0)
        if py < by:
            self.move_col_box(0, by - py + 1)
        if py + ph > by + bh:
            self.move_col_box(0, -py - ph + by + bh - 1)

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

    def update_state(self, lag):
        deltas = self.__calculate_movement_deltas(lag, 0)
        self.__player_box = self.__player_box.move(deltas[0], deltas[1])
        # both speeds form a vector, according to its angle, adjust rotation
        # need to transform to degrees
        if self.__current_speed_y != 0 or self.__current_speed_x != 0:
            self.__orientation = math.atan2(self.__current_speed_y, self.__current_speed_x) * 57.2958
            if self.__orientation < 0:
                self.__orientation = 360 + self.__orientation
            self.__orientation = float((self.__orientation + 92) % 360)
        self.__update_state_invul(lag)

        if (self.__acceleration_y != 0 or self.__acceleration_x != 0) and not self.__is_playing:
            self.__engine_sound.set_volume(self.__audio.get_gobal_volume())
            self.__engine_sound.play(-1)
            self.__is_playing = True
        elif self.__acceleration_y == 0 and self.__acceleration_x == 0 and self.__is_playing:
            self.__engine_sound.set_volume(self.__audio.get_gobal_volume())
            self.__engine_sound.stop()
            self.__is_playing = False

    def render(self, percentage, graphics, camera=None, sprite_sheet_box=None):
        # do something with camera
        # encapsulate drawing to drawable
        if self.__state == "alive":
            deltas = self.__calculate_movement_deltas(0, percentage)
            self.__player_box = self.__player_box.move(deltas[0], deltas[1])

            # according to rotation, select correct sprite
            sprite_number = self.__orientation // 15
            x, y = sprite_number % 5, sprite_number // 5
            size = 830 // 5
            sprite_sheet_box = pygame.Rect(x * size, y * size, size, size)

            self.set_image(self.sprite)
            self.set_position(self.__player_box.left, self.__player_box.top)
            self.set_dimensions((self.__player_box.width, self.__player_box.height))

            # delegate to drawable
            if self.__invulnerable_ms_left == 0:
                super().render(percentage, graphics, camera, sprite_sheet_box)
            else:
                if self.__inv_toggle:
                    super().render(percentage, graphics, camera, sprite_sheet_box)
                self.__inv_toggle = not self.__inv_toggle
        else:
            size = 256
            self.set_image(Sprite(self.__sprite_sheet_dead[self.__death_sprite_number]))
            self.set_position(self.__player_box.left, self.__player_box.top)
            self.set_dimensions((size, size))
            super().render(percentage, graphics, camera)
            self.__death_sprite_number = (self.__death_sprite_number + 1) % 25

    def accelerate(self, x=None, y=None):
        if x is not None:
            self.__acceleration_x = x
        if y is not None:
            self.__acceleration_y = y

    def hurt(self, damage):
        self.__hit_points = self.__hit_points - damage
        self.__invulnerable_ms_left = 1000

    def kill(self):
        self.__state = "dead"
        self.stop_movement()
        self.stop_sounds()

    def is_vulnerable(self):
        return self.__invulnerable_ms_left == 0

    def __update_state_invul(self, lag):
        self.__invulnerable_ms_left = self.__invulnerable_ms_left - lag
        if self.__invulnerable_ms_left < 0:
            self.__invulnerable_ms_left = 0

    def stop_movement(self):
        self.__acceleration_y = 0
        self.__acceleration_x = 0

    def stop_sounds(self):
        if self.__is_playing:
            self.__engine_sound.stop()
            self.__is_playing = False

    def is_dead(self):
        return self.__hit_points <= 0

    def get_max_hp(self):
        return self.__max_hit_points

    def disable_collision(self):
        self.__collision_enabled = False

    def enable_collision(self):
        self.__collision_enabled = True

    def is_touching(self, other) -> bool:
        if self.__collision_enabled:
            return super().is_touching(other)
        return self.__collision_enabled

    def get_speed_vector(self) -> (float, float):
        return math.sin(self.__orientation*0.0174533), -math.cos(self.__orientation*0.0174533)

    def get_position(self) -> (int, int):
        return self.__player_box.left, self.__player_box.top

    def get_center(self) -> (int, int):
        return self.__player_box.center

    def is_done(self):
        return False
