import math
import queue
import time
from threading import Thread

from devsancabo.input import Event
from queue import Queue

enemies_top = list(range(1, 100, 2))
enemies_left = list(range(1, 100, 2))

scenario_events = [
    (0, Event("spawn_enemy_lineal_wave", ["top", 15]))#,
    #(0.5, Event("spawn_enemy_lineal_wave", ["left", 15]))
]


def init_timed_events(event_queue: Queue):
    scan_thread = Thread(target=scan, args=(event_queue,))
    scan_thread.start()
    return


# todo encapsulate timer on an object. Kill threads on destroy
def stop_timed_events():
    pass


def scan(event_queue: Queue):
    time.sleep(10)
    start = now()
    for i, timed_event in enumerate(scenario_events):
        done = False
        while not done:
            elapsed = now() - start
            if elapsed / 1000 >= timed_event[0]:
                done = True
                event_queue.put(timed_event[1])

def now():
    return math.floor(time.time() * 1000)
