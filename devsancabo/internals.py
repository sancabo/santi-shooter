import queue
from abc import abstractmethod

from devsancabo.graphics import Graphics
from devsancabo.input import Event


class GameState:
    def __init__(self, events: queue.Queue, state_queue: queue.LifoQueue):
        self.event_queue = events
        self.events_handled = 0
        self.__state_queue = state_queue
        self.__terminated = False
        self.elapsed_millis = 0

    def update_logic(self, lag):
        self.elapsed_millis = self.elapsed_millis + lag
        self.__state_queue.put(self)
        self.on_update(lag)
        while not self.event_queue.empty() and not self.__terminated:
            event: Event = self.event_queue.get_nowait()
            self.handle_event(event)

    def render(self, percentage: float, graphics: Graphics):
        self.render_internal(percentage, graphics)

    def go_previous_state(self):
        self.__state_queue.get_nowait()

    def go_to_state(self, new_state):
        self.__state_queue.put(new_state)

    @abstractmethod
    def render_internal(self, percentage: float, graphics: Graphics):
        pass

    @abstractmethod
    def handle_event_internal(self, event: Event):
        pass

    @abstractmethod
    def on_update(self, lag):
        pass

    def handle_event(self, event: Event):
        match event:
            case "hardEscape":
                self.events_handled = self.events_handled + 1
                self.__state_queue.get_nowait()
                self.__terminated = True
                print("handled event {0}".format(event))
            case _:
                self.handle_event_internal(event)

    def alt_f4(self):
        while not self.__state_queue.empty():
            self.__state_queue.get_nowait()
        self.__state_queue.put(NullGameState())


class NullGameState(GameState):

    def __init__(self):
        GameState.__init__(self, queue.Queue(), queue.LifoQueue())

    def render_internal(self, percentage: float, graphics):
        # will never be called
        raise GameClosedException()

    def on_update(self, lag):
        raise GameClosedException()

    def handle_event_internal(self, event):
        # will never be called
        raise GameClosedException()


class GameClosedException(Exception):
    pass
