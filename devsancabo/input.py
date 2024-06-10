from pynput import keyboard
import queue


class InputListener:
    bindings = {keyboard.Key.enter: "shoot", keyboard.Key.esc: "escape"}

    def __init__(self, event_queue: queue.Queue):
        self.event_queue = event_queue

    def start_keyboard_listener(self):
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        listener.start()

    def on_press(self, key):
        if key in InputListener.bindings:
            self.event_queue.put(InputListener.bindings[key])

    def on_release(self, key):
        pass
