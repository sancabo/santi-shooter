import decimal
import queue
from abc import abstractmethod


class GameState:
    def __init__(self, events: queue.Queue, state_queue: queue.LifoQueue):
        self.event_queue = events
        self.events_handled = 0
        self.state_queue = state_queue
        self.terminated = False

    def update_logic(self):
        self.state_queue.put(self)
        while not self.event_queue.empty() and not self.terminated:
            event = self.event_queue.get_nowait()
            self.handle_event(event)

    def render(self, percentage: float):
        # as_decimal = decimal.Decimal(percentage * 100)
        # print("Render: Adelantar movimiento de entidades by " + round(as_decimal, 2).__str__() + "%")
        self.render_internal(percentage)

    @abstractmethod
    def render_internal(self,  percentage: float):
        pass

    @abstractmethod
    def handle_event_internal(self, event):
        pass

    def handle_event(self, event):
        match event:
            case "hardEscape":
                self.events_handled = self.events_handled + 1
                self.state_queue.get_nowait()
                self.terminated = True
                print("handled event {0}".format(event))
            case _: self.handle_event_internal(event)

    def __del__(self):
        print("handled {0} enter events".format(self.events_handled))


class NullGameState(GameState):

    def __init__(self, events: queue.Queue, state_queue: queue.LifoQueue):
        GameState.__init__(self, events, state_queue)

    def render_internal(self,  percentage: float):
        # will never be called
        raise GameClosedException()

    def handle_event_internal(self, event):
        # will never be called
        raise GameClosedException()


class GameClosedException(Exception):
    pass
