from queue import Queue, LifoQueue

import pygame

from devsancabo.audio import Audio
from devsancabo.entities.player import Player
from devsancabo.entities.text import Text
from devsancabo.gamestates.base_game_states import GameState, NullGameState
from devsancabo.graphics import SceneTreeLayer, Graphics
from devsancabo.input import Event

GOLDEN_YELLOW_RGB = (255, 200, 100)


class Gameover(GameState):

    def __init__(self,
                 events: Queue,
                 state_queue: LifoQueue,
                 audio: Audio,
                 player: Player,
                 state: GameState,
                 viewport : tuple[int, int],
                 screen_bounds: (int, int, int, int)):
        super().__init__(events, state_queue, audio)
        self.__elapsed = 0
        self.__done = False
        self.__player = player
        self.__scene_tree = SceneTreeLayer()
        self.__screen_bounds = screen_bounds
        print("Game over.")
        pygame.mixer.music.fadeout(2000)
        self.__player.stop_sounds()
        self.__player.stop_movement()
        self.__player.disable_collision()
        self.__audio = audio
        self.__audio.play_sound("assets/catching-fire.mp3", 0)
        self.__player.kill()
        self.__prev = state
        self.__viewport = viewport

    def render_internal(self, percentage: float, graphics: Graphics):
        self.__prev.render_internal(percentage, graphics)
        self.__scene_tree.render(percentage, graphics)

    def handle_event_internal(self, event: Event):
        match event.name:
            case "escape":
                self.alt_f4()
            case "restart":
                self.alt_f4()
                self.go_to_state(self.__prev.get_reset_state())

    def on_update(self, lag):
        self.__elapsed = self.__elapsed + lag
        if self.__elapsed >= 2000 and not self.__done:
            self.__audio.play_sound("assets/game-over.wav")
            self.__scene_tree.create_group("gameover", 10)
            box = pygame.Rect(self.__screen_bounds)
            box = box.move(0, - self.__screen_bounds[3]/4)
            self.__scene_tree.add_to_group(
                Text("You died! Press Esc to leave or R to restart", 60, box.center,
                     GOLDEN_YELLOW_RGB, (4, (0, 0, 0))),
                "gameover")
            self.__done = True

    def is_done(self):
        return self.__done
