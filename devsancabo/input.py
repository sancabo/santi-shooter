import math
import queue
import time

from pynput import keyboard
from pynput import mouse


class Event:
    def __init__(self, name, params=None):
        if params is None:
            params = []
        self.name = name
        self.params = params


class InputListener:
    bindings = {keyboard.Key.enter: [Event("shoot"), Event("stop-shooting")],
                mouse.Button.left: [Event("shoot"), Event("stop-shooting")],
                keyboard.Key.esc: [Event("escape"), Event("after-escape")],
                keyboard.Key.down: [Event("move-down"), Event("stop-move-down")],
                keyboard.KeyCode.from_char("s"): [Event("move-down"), Event("stop-move-down")],
                keyboard.Key.up: [Event("move-up"), Event("stop-move-up")],
                keyboard.KeyCode.from_char("w"): [Event("move-up"), Event("stop-move-up")],
                keyboard.Key.left: [Event("move-left"), Event("stop-move-left")],
                keyboard.KeyCode.from_char("a"): [Event("move-left"), Event("stop-move-left")],
                keyboard.Key.right: [Event("move-right"), Event("stop-move-right")],
                keyboard.KeyCode.from_char("d"): [Event("move-right"), Event("stop-move-right")],
                keyboard.Key.space: [Event("pause"), Event("null")],
                }

    cooldown_map = {
        keyboard.Key.enter: 0,
        mouse.Button.left: 0,
        keyboard.Key.esc: 0,
        keyboard.Key.down: 0,
        keyboard.KeyCode.from_char("s"): 0,
        keyboard.Key.up: 0,
        keyboard.KeyCode.from_char("w"): 0,
        keyboard.Key.left: 0,
        keyboard.KeyCode.from_char("a"): 0,
        keyboard.Key.right: 0,
        keyboard.KeyCode.from_char("d"): 0,
        keyboard.Key.space: 0
    }

    def __init__(self, event_queue: queue.Queue):
        self.event_queue = event_queue
        for key in self.cooldown_map.keys():
            self.cooldown_map[key] = self.now()

    def test_rebinding(self, event_name, key) -> bool:
        # search an entry that has entry.value = event_name
        # if not exists, error "event doesn't exist"
        # else, delete it
        # search an entry that has entry.key = key
        # return entry != null
        return False

    def re_bind(self, event_name, key):
        if self.test_rebinding(event_name, key):
            InputListener.bindings[key] = (Event(event_name), Event(event_name))

    def start_keyboard_listener(self):
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        listener.start()

    def start_mouse_listener(self):
        listener_mouse = mouse.Listener(
            on_click=self.on_click)
        listener_mouse.start()

    def on_press(self, key: keyboard.Key):
        if key in InputListener.bindings:
            self.event_queue.put(InputListener.bindings[key][0])

    def on_release(self, key: keyboard.Key):
        if key in InputListener.bindings:
            if self.now() - self.cooldown_map[key] > 50:
                self.event_queue.put(InputListener.bindings[key][1])
            self.cooldown_map[key] = self.now()

    def on_click(self, x, y, button, pressed):
        if pressed and button in InputListener.bindings:
            self.event_queue.put(InputListener.bindings[button][0])

    @staticmethod
    def now() -> int:
        # current time in millis
        return math.floor(time.time() * 1000)
