import queue
import time
import math
import pygame
from queue import Queue

from devsancabo.gamestates.first_level import FirstLevel
from devsancabo.graphics import Graphics
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
        self.is_running = True

        # I read that a state machine that saves the current state to a stack is called a
        # push down automata? It adds the possibility of remembering previous states.
        # so we can use it to navigate "screens" and "menus"
        self.game_state_stack = queue.LifoQueue(maxsize=99)

    @staticmethod
    def now() -> int:
        # current time in millis
        return math.floor(time.time() * 1000)

    def run(self):
        graphics = Graphics()

        input_listener = InputListener(self.event_queue)
        input_listener.start_mouse_listener()
        input_listener.start_keyboard_listener()
        self.game_state_stack.put(NullGameState(self.event_queue, self.game_state_stack))
        self.game_state_stack.put(FirstLevel(self.event_queue, self.game_state_stack))

        while self.is_running:
            self.lag = self.calculate_lag()
            self.lag_render = self.lag

            try:
                while self.lag >= Game.__MS_PER_UPDATE:
                    current_game_state: GameState = self.game_state_stack.get_nowait()
                    current_game_state.update_logic()
                    self.lag -= Game.__MS_PER_UPDATE

                if current_game_state is not None and self.lag_render >= Game.__MIN_MS_PER_RENDER:
                    graphics.screen.fill("black")
                    current_game_state.render(self.lag / Game.__MS_PER_UPDATE, graphics)
                    graphics.show()

            except GameClosedException:
                self.is_running = False
                continue

        pygame.quit()

    def calculate_lag(self) -> int:
        current = Game.now()
        elapsed = current - self.previous
        self.previous = current
        return elapsed + self.lag

    def __del__(self):
        print("Exiting game. Goodbye \n")


Game().run()