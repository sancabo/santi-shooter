import math
import queue
import time
from threading import Thread

from devsancabo.input import Event
from queue import Queue

enemies_top = list(range(1, 100, 1))
enemies_left = list(range(1, 100, 1))


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
    (92, Event("spawn_enemy_lineal_wave", ["bottom", 15]))
]


def init_timed_events(event_queue: Queue):
    scan_thread = Thread(target=scan, args=(event_queue,))
    scan_thread.start()
    return

def stop_timed_events():
    pass

# todo add ability to stop this thread on game exit
def scan(event_queue: Queue):
    previous = 0
    for event in scenario_events:
        time.sleep(event[0] - previous)
        event_queue.put(event[1])
        previous = event[0]

def now():
    return math.floor(time.time() * 1000)
