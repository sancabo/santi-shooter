from devsancabo.entities.enemy import Enemy


ONE_SECOND_MS = 1000


class EnemySpawner:
    def __init__(self, delay, direction, bounds, occurrences=1, terminate_after_sec=10):
        self.__delay = delay
        self.__direction = direction
        self.__occurrences = occurrences
        self.__spawned = 0
        self.__elapsed = 0
        self.__idle_lifetime = 0
        self.__terminate_after_sec = terminate_after_sec
        self.__bounds = bounds
        self.__total_produced_enemies = []
        self.__produced_enemies = []

    def update_state(self, lag):
        if self.__spawned < self.__occurrences:
            self.__elapsed = self.__elapsed + lag
            if self.__elapsed / ONE_SECOND_MS >= self.__delay:
                self.__elapsed = self.__elapsed / ONE_SECOND_MS - self.__delay
                self.__spawn_enemy_generic(self.__direction, self.__spawned)
                self.__spawned = self.__spawned + 1
        else:
            self.__idle_lifetime = self.__idle_lifetime + lag

    def get_produced_enemies(self) -> [Enemy]:
        result = self.__produced_enemies.copy()
        for e in result:
            self.__total_produced_enemies.append(e)
        self.__produced_enemies.clear()
        return result

    def get_total_produced_enemies(self):
        return self.__total_produced_enemies

    def is_terminated(self):
        return self.__idle_lifetime / ONE_SECOND_MS >= self.__terminate_after_sec

    def __spawn_enemy_generic(self, enter_direction, offset):
        spacing = 150
        out_of_bounds_distance = 300
        speed = 1100
        match enter_direction:

            case "top":
                enemy_position = (spacing * offset, self.__bounds.get_col_box()[1] - out_of_bounds_distance)
                accel = (0, speed)
            case "bottom":
                enemy_position = (
                    spacing * offset, self.__bounds.get_col_box()[1] + self.__bounds.get_col_box()[3] + out_of_bounds_distance)
                accel = (0, -speed)
            case "left":
                enemy_position = (self.__bounds.get_col_box()[0] - out_of_bounds_distance, spacing * offset)
                accel = (speed, 0)
            case "right":
                enemy_position = (
                    self.__bounds.get_col_box()[0] + self.__bounds.get_col_box()[2] + out_of_bounds_distance, spacing * offset)
                accel = (-speed, 0)
            case _:
                print("Error: called 'spawn enemy' without 'direction' argument")
                enemy_position = (-500, -500)
                accel = (0, 0)

        enemy = Enemy(750, 600)
        enemy.relocate_col_box(enemy_position[0], enemy_position[1])
        enemy.accelerate(y=accel[1], x=accel[0])
        self.__produced_enemies.append(enemy)
