import queue
from abc import abstractmethod

from devsancabo.entities.base import Collisionable
from devsancabo.graphics import Graphics


class GameState:
    def __init__(self, events: queue.Queue, state_queue: queue.LifoQueue):
        self.__event_queue = events
        self.events_handled = 0
        self.__state_queue = state_queue
        self.__terminated = False
        self.elapsed_millis = 0

    def update_logic(self, lag):
        self.elapsed_millis = self.elapsed_millis + lag
        self.__state_queue.put(self)
        self.on_update(lag)
        while not self.__event_queue.empty() and not self.__terminated:
            event = self.__event_queue.get_nowait()
            self.handle_event(event)

    def render(self, percentage: float, graphics: Graphics):
        self.render_internal(percentage, graphics)

    @abstractmethod
    def render_internal(self, percentage: float, graphics: Graphics):
        pass

    @abstractmethod
    def handle_event_internal(self, event):
        pass

    @abstractmethod
    def on_update(self, lag):
        pass

    @abstractmethod
    def get_collision_entities(self) -> [Collisionable]:
        pass

    def handle_event(self, event):
        match event:
            case "hardEscape":
                self.events_handled = self.events_handled + 1
                self.__state_queue.get_nowait()
                self.__terminated = True
                print("handled event {0}".format(event))
            case _:
                self.handle_event_internal(event)

    def __del__(self):
        print("handled {0} enter events".format(self.events_handled))


class NullGameState(GameState):

    def get_collision_entities(self) -> [Collisionable]:
        raise GameClosedException()

    def __init__(self, events: queue.Queue, state_queue: queue.LifoQueue):
        GameState.__init__(self, events, state_queue)

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
