import decimal
import queue
import time

from devsancabo.internals import GameState


class FirstLevel(GameState):
    def __init__(self, events: queue.Queue, state_queue: queue.LifoQueue):
        GameState.__init__(self, events, state_queue)

    # top speed
    # current speedX
    # current speedY
    # accelerationX
    # accelerationY
    # positionX
    # positionY
    # speed is pixels per millisecond
    # I know one update cycle is supposed to be 17ms
    # only the last moveX command per cycle is executed.
    def handle_event_internal(self, event):
        match event:
            case "shoot":
                self.events_handled = self.events_handled + 1
                print("handled event {0}".format(event))
            case "escape":
                self.events_handled = self.events_handled + 1
                self.state_queue.get_nowait()  # this means "go back to previous state"
                self.terminated = True
                print("handled event {0}".format(event))
            case _:
                print("cannot handle event {0}".format(event))

    def render_internal(self, percentage: decimal.Decimal):
        time.sleep(0.010)
