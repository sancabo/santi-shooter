import string

from pynput import keyboard
from pynput import mouse
import queue


class Event:
    def __init__(self, name, params=None):
        if params is None:
            params = []
        self.name = name
        self.params = params


class InputListener:
    bindings = {keyboard.Key.enter:                 [Event("shoot"), Event("stop-shooting")],
                mouse.Button.left:                  [Event("shoot"), Event("stop-shooting")],
                keyboard.Key.esc:                   [Event("escape"), Event("after-escape")],
                keyboard.Key.down:                  [Event("move-down"), Event("stop-move-down")],
                keyboard.KeyCode.from_char("s"):    [Event("move-down"), Event("stop-move-down")],
                keyboard.Key.up:                    [Event("move-up"), Event("stop-move-up")],
                keyboard.KeyCode.from_char("w"):    [Event("move-up"), Event("stop-move-up")],
                keyboard.Key.left:                  [Event("move-left"), Event("stop-move-left")],
                keyboard.KeyCode.from_char("a"):    [Event("move-left"), Event("stop-move-left")],
                keyboard.Key.right:                 [Event("move-right"), Event("stop-move-right")],
                keyboard.KeyCode.from_char("d"):    [Event("move-right"), Event("stop-move-right")],
                keyboard.Key.space:                 [Event("pause"), Event("null")],
                }

    def __init__(self, event_queue: queue.Queue):
        self.event_queue = event_queue

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
            self.event_queue.put(InputListener.bindings[key][1])

    def on_click(self, x, y, button, pressed):
        if pressed and button in InputListener.bindings:
            self.event_queue.put(InputListener.bindings[button][0])
