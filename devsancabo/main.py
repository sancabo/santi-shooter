import queue
import time
import math
import pygame
from queue import Queue

from devsancabo.gamestates.first_level import FirstLevel
from devsancabo.graphics import Graphics
from devsancabo.input import InputListener
from devsancabo.internals import GameState, NullGameState, GameClosedException

MS_PER_UPDATE = 17
MIN_MS_PER_RENDER = 5

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 1020

class Game:
    # todo implement sound
    # for 60 times per second, we have to configure 17 ms per update
    __MS_PER_UPDATE = MS_PER_UPDATE
    # controls max fps. 0 for unlimited. 33 for 30 fps. 5 for 200 fps
    __MIN_MS_PER_RENDER = MIN_MS_PER_RENDER

    def __init__(self):
        self.lag_render: int = 0
        self.previous: int = Game.now()
        self.lag: int = 0
        self.event_queue = Queue()
        self.is_running = True
        self.game_state_stack = queue.LifoQueue()

    @staticmethod
    def now() -> int:
        # current time in millis
        return math.floor(time.time() * 1000)

    def run(self):
        graphics = Graphics(SCREEN_WIDTH, SCREEN_HEIGHT)
        input_listener = InputListener(self.event_queue)
        input_listener.start_mouse_listener()
        input_listener.start_keyboard_listener()
        self.game_state_stack.put(NullGameState(self.event_queue, self.game_state_stack))
        self.game_state_stack.put(FirstLevel(self.event_queue, self.game_state_stack))

        while self.is_running:
            self.lag = self.calculate_lag()
            self.lag_render = self.lag
            updated = False
            try:
                while self.lag >= Game.__MS_PER_UPDATE:
                    current_game_state: GameState = self.game_state_stack.get_nowait()
                    current_game_state.update_logic(Game.__MS_PER_UPDATE)
                    self.lag -= Game.__MS_PER_UPDATE
                    updated = True

                if updated and self.lag_render >= Game.__MIN_MS_PER_RENDER:
                    current_game_state.render(self.lag / Game.__MS_PER_UPDATE, graphics)
                    graphics.print_screen()
                pygame.event.pump()

            except GameClosedException:
                self.is_running = False
                continue

    def calculate_lag(self) -> int:
        current = Game.now()
        elapsed = current - self.previous
        self.previous = current
        return elapsed + self.lag

    def __del__(self):
        pygame.quit()
        print("Exiting game. Goodbye \n")


Game().run()
