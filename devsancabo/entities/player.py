import pygame

from devsancabo.graphics import Graphics


# Implements Drawable, for the scene tree
# The scene tree only knows Drawable objects
# Can we abstract the physics. Activate/Deactivate velocity/acceleration. By inheritance or composition?
class Player:
    def __init__(self):
        # Translate in-game coordinates to screen coordinates
        # Leads to implementation of camera.
        # Separate physics calculations into a physics module
        self.__player_pos = [0, 0]
        self.__top_speed = 0.03
        self.__current_speed_x = 0
        self.__current_speed_y = 0
        self.__acceleration_x = 0
        self.__acceleration_y = 0
        self.__natural_friction = 0.00003

        # Moveable.apply_accel(accel, residual_lag)
        #   accel how much coord/millisecond I want to modify the speed each ms
        #   residual_lag value to add to #update_lag
        # Moveable.set_top_speed(top_speed)
        # Moveable.set_slippery_scale(slippery_scale)
        # Moveable(update_lag, slippery_scale = 1, top_speed = 1)
        #   update_lag used to scale speed and acceleration for calculation
        #   maximum coord/millisecond this entity can move
        #   slippery_scale how much of it's speed it loses each at stop, and each update

    def calculate_movement_deltas(self, percentage):
        # change logic, when acceleration is 0, apply friction
        # otherwise, ignore it
        new_speed_y = self.__current_speed_y + self.__acceleration_y
        if new_speed_y > 0:
            new_speed_y = new_speed_y - self.__natural_friction
        else:
            new_speed_y = new_speed_y + self.__natural_friction

        new_speed_x = self.__current_speed_x + self.__acceleration_x
        if new_speed_x > 0:
            new_speed_x = new_speed_x - self.__natural_friction
        else:
            new_speed_x = new_speed_x + self.__natural_friction

        if self.__top_speed > new_speed_y.__abs__():
            self.__current_speed_y = new_speed_y
        else:
            if new_speed_y > 0:
                self.__current_speed_y = self.__top_speed
            else:
                self.__current_speed_y = - self.__top_speed

        if self.__top_speed > new_speed_x.__abs__():
            self.__current_speed_x = new_speed_x
        else:
            if new_speed_x > 0:
                self.__current_speed_x = self.__top_speed
            else:
                self.__current_speed_x = - self.__top_speed

        return (self.__current_speed_x * float(17 + (17 * percentage)),
                self.__current_speed_y * float(17 + (17 * percentage)))

    def render(self, percentage, graphics: Graphics):
        deltas = self.calculate_movement_deltas(percentage)
        graphics.draw_entity(pygame.Rect(self.__player_pos[0], self.__player_pos[1], 40, 40), deltas)
        x, y = deltas
        self.__player_pos = [self.__player_pos[0] + x,
                             self.__player_pos[1] + y]

    def move_down(self):
        self.__acceleration_y = 0.0001

    def move_up(self):
        self.__acceleration_y = -0.0001

    def move_left(self):
        self.__acceleration_x = -0.0001

    def move_right(self):
        self.__acceleration_x = 0.0001

    def stop_move_down(self):
        self.__acceleration_y = 0

    def stop_move_up(self):
        self.__acceleration_y = 0

    def stop_move_left(self):
        self.__acceleration_x = 0

    def stop_move_right(self):
        self.__acceleration_x = 0
