import math
from queue import Queue

from devsancabo.input import Event

scenario_events = [
    (0, Event("spawn_enemy_lineal_wave", ["top", 15])),
    (5, Event("spawn_enemy_lineal_wave", ["left", 15])),
    (10, Event("spawn_enemy_lineal_wave", ["right", 15])),
    (15, Event("spawn_enemy_lineal_wave", ["bottom", 15])),
    (30, Event("spawn_enemy_lineal_wave", ["top", 15])),
    (31, Event("spawn_enemy_lineal_wave", ["bottom", 15])),
    (33, Event("spawn_enemy_lineal_wave", ["top", 15])),
    (34, Event("spawn_enemy_lineal_wave", ["bottom", 15])),
    (50, Event("spawn_enemy_lineal_wave", ["left", 15])),
    (51, Event("spawn_enemy_lineal_wave", ["right", 15])),
    (53, Event("spawn_enemy_lineal_wave", ["left", 15])),
    (54, Event("spawn_enemy_lineal_wave", ["right", 15])),
    (65, Event("spawn_enemy_lineal_wave", ["top", 15])),
    (66, Event("spawn_enemy_lineal_wave", ["left", 15])),
    (67, Event("spawn_enemy_lineal_wave", ["right", 15])),
    (68, Event("spawn_enemy_lineal_wave", ["bottom", 15])),
    (69, Event("spawn_enemy_lineal_wave", ["top", 15])),
    (70, Event("spawn_enemy_lineal_wave", ["left", 15])),
    (71, Event("spawn_enemy_lineal_wave", ["right", 15])),
    (82, Event("spawn_enemy_lineal_wave", ["bottom", 15])),
    (85, Event("spawn_enemy_lineal_wave", ["top", 15])),
    (86, Event("spawn_enemy_lineal_wave", ["left", 15])),
    (87, Event("spawn_enemy_lineal_wave", ["right", 15])),
    (88, Event("spawn_enemy_lineal_wave", ["bottom", 15])),
    (89, Event("spawn_enemy_lineal_wave", ["top", 15])),
    (90, Event("spawn_enemy_lineal_wave", ["left", 15])),
    (91, Event("spawn_enemy_lineal_wave", ["right", 15])),
    (92, Event("spawn_enemy_lineal_wave", ["bottom", 15])),
    (93, Event("spawn_enemy_random_direction", [45, 0.5])),
    (100, Event("spawn_enemy_random_direction", [30, 0.4])),
    (107, Event("spawn_enemy_random_direction", [15, 0.2])),
    (121, Event("stage_cleared", []))
]

scenario_events_2 = [
    (600, Event("stage_cleared", []))]

scenario_events_3 = [
    (1, Event("spawn_enemy_random_direction", [0.5, 45])),
    (23, Event("spawn_enemy_random_direction", [0.4, 30])),
    (35, Event("spawn_enemy_random_direction", [0.2, 45])),
    (44, Event("spawn_enemy_random_direction", [0.1, 45])),
    (50, Event("spawn_enemy_random_direction", [0.03, 200])),
    (56, Event("stage_cleared", []))]


class TimedEvents:
    def __init__(self, event_queue: Queue):
        self.__event_queue = event_queue
        self.__previous = 0
        self.__elapsed = 0
        self.__events = scenario_events_2

    def update_state(self, lag: int):
        self.__elapsed = self.__elapsed + lag
        if (self.__previous < len(self.__events) and
                self.__elapsed / 1000 >= self.__events[self.__previous][0]):
            self.__event_queue.put(self.__events[self.__previous][1])
            self.__previous = self.__previous + 1

    def is_done(self) -> bool:
        return self.__previous >= len(self.__events)
