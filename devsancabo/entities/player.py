from devsancabo.graphics import Graphics


#Implements Rendereable, for the scene tree
#The scene tree only knows Rendereable objects
#Can we abtract the physics. Activate/Deactivate velocity/acceleration. By inheritance or composition?
class Player:
    def __init__(self):
        # Translate in-game coordinates to screen coordinates
        # Leads to implementation of camera.
        # Separate physics calculations into a physics module
        self.player_pos = [0, 0]
        self.top_speed = 0.03
        self.current_speed_x = 0
        self.current_speed_y = 0
        self.acceleration_x = 0
        self.acceleration_y = 0
        self.natural_friction = 0.00003

    def render(self,  percentage, graphics: Graphics):
        x, y = self.player_pos

        new_speed_y = self.current_speed_y + self.acceleration_y
        if new_speed_y > 0:
            new_speed_y = new_speed_y - self.natural_friction
        else:
            new_speed_y = new_speed_y + self.natural_friction

        new_speed_x = self.current_speed_x + self.acceleration_x
        if new_speed_x > 0:
            new_speed_x = new_speed_x - self.natural_friction
        else:
            new_speed_x = new_speed_x + self.natural_friction

        if self.top_speed > new_speed_y.__abs__():
            self.current_speed_y = new_speed_y
        else:
            if new_speed_y > 0:
                self.current_speed_y = self.top_speed
            else:
                self.current_speed_y = - self.top_speed

        if self.top_speed > new_speed_x.__abs__():
            self.current_speed_x = new_speed_x
        else:
            if new_speed_x > 0:
                self.current_speed_x = self.top_speed
            else:
                self.current_speed_x = - self.top_speed
        y = y + self.current_speed_y * float(17 + (17 * percentage))
        x = x + self.current_speed_x * float(17 + (17 * percentage))
        self.player_pos = [x, y]
        graphics.draw_circle("red", self.player_pos, 40)
