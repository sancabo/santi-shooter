from pynput import keyboard
from pynput import mouse
import queue


class InputListener:
    bindings = {keyboard.Key.enter: ["shoot", "stop-shooting"],
                mouse.Button.left: ["shoot", "stop-shooting"],
                keyboard.Key.esc: ["escape", "after-escape"],
                keyboard.Key.down: ["move-down", "stop-move-down"],
                keyboard.KeyCode.from_char("s"): ["move-down", "stop-move-down"],
                keyboard.Key.up: ["move-up", "stop-move-up"],
                keyboard.KeyCode.from_char("w"): ["move-up", "stop-move-up"],
                keyboard.Key.left: ["move-left", "stop-move-left"],
                keyboard.KeyCode.from_char("a"): ["move-left", "stop-move-left"],
                keyboard.Key.right: ["move-right", "stop-move-right"],
                keyboard.KeyCode.from_char("d"): ["move-right", "stop-move-right"],
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
