import math
from queue import Queue, LifoQueue

import pygame
from pygame import Color

from devsancabo.audio import Audio
from devsancabo.entities.text import Text
from devsancabo.graphics import Graphics, Sprite, Drawable, SceneTreeLayer
from devsancabo.input import Event
from devsancabo.gamestates.base_game_states import GameState


class PauseMenu(GameState):
    def __init__(self, events: Queue, state_queue: LifoQueue, audio: Audio,
                 scene_tree: SceneTreeLayer, center: (int, int), previous_game_state: GameState = None):
        self.__scene: [Drawable] = []
        self.__center = center
        self.__scene_tree = scene_tree
        self.__scene_tree.create_group("pause", 10)
        self.previous_game_state = previous_game_state
        self.__scene_tree.add_to_group(self.generate_rectangle(), "pause")
        self.__scene_tree.add_to_group(Text("PAUSE", 60, center, (255, 255, 255), (4, (255, 75, 40))), "pause")
        super().__init__(events, state_queue, audio)

    def render_internal(self, percentage: float, graphics: Graphics):
        self.__scene_tree.render(percentage, graphics)

    def generate_rectangle(self) -> Drawable:
        rect = pygame.Rect(500, 500, 750, 500)
        rect.center = self.__center
        box = pygame.Surface((750, 500))
        opacity = 0.5
        pygame.Surface.fill(box, Color(0, 0, 0))
        box.set_alpha(math.floor(255 * opacity))
        return Drawable(Sprite(box), rect.left, rect.top, rect.width, rect.height)

    def handle_event_internal(self, event: Event):
        match event.name:
            case "pause" | "escape":
                self.__scene_tree.remove_group("pause")
                self.go_previous_state()

    def on_update(self, lag):
        pass
