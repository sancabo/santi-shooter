import queue
import time
import math
from queue import Queue

from devsancabo.first_level import FirstLevel
from devsancabo.input import InputListener
from devsancabo.internals import GameState, NullGameState, GameClosedException


class Game:
    # for 60 times per second, we have to configure 17 ms per update
    __MS_PER_UPDATE = 17
    # controls max fps. 0 for unlimited. 33 for 30 fps. 5 for 200 fps
    __MIN_MS_PER_RENDER = 5

    def __init__(self):
        self.lag_render: int = 0
        self.previous: int = Game.now()
        self.lag: int = 0
        self.event_queue = Queue()
        self.isRunning = True

        # I read that a state machine that saves the current state to a stack is called a
        # push down automata? It adds the possibility of remembering previous states.
        # so we can use it to navigate "screens" and "menus"
        self.game_state_stack = queue.LifoQueue(maxsize=99)

    @staticmethod
    def now() -> int:
        # current time in millis
        return math.floor(time.time() * 1000)

    def run(self):
        InputListener(self.event_queue).start_keyboard_listener()
        self.game_state_stack.put(NullGameState(self.event_queue, self.game_state_stack))
        self.game_state_stack.put(FirstLevel(self.event_queue, self.game_state_stack))

        while self.isRunning:
            self.lag = self.calculate_lag()
            self.lag_render = self.lag

            try:
                while self.lag >= Game.__MS_PER_UPDATE:
                    current_game_state: GameState = self.game_state_stack.get_nowait()
                    current_game_state.update_logic()
                    self.lag -= Game.__MS_PER_UPDATE

                if current_game_state is not None and self.lag_render >= Game.__MIN_MS_PER_RENDER:
                    current_game_state.render(self.lag / Game.__MS_PER_UPDATE)

            except GameClosedException:
                self.isRunning = False
                continue

    def calculate_lag(self) -> int:
        current = Game.now()
        elapsed = current - self.previous
        self.previous = current
        return elapsed + self.lag

    def __del__(self):
        print("Exiting game. Goodbye \n")


Game().run()
