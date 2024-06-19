import math
from queue import Queue, LifoQueue

import pygame
from pygame import Color

from devsancabo.audio import Audio
from devsancabo.entities.text import Text
from devsancabo.graphics import Graphics, Sprite, Drawable
from devsancabo.input import Event
from devsancabo.gamestates.base_game_states import GameState


class PauseMenu(GameState):
    def __init__(self, events: Queue, state_queue: LifoQueue, audio: Audio,
                 previous_game_state: GameState = None, center: (int, int) = (0, 0), ):
        self.__scene: [Drawable] = []
        self.__scene.append(Text("PAUSE", 60, center, (255, 255, 255), (4, (255, 75, 40))))
        self.__center = center
        self.previous_game_state = previous_game_state
        super().__init__(events, state_queue, audio)

    def render_internal(self, percentage: float, graphics: Graphics):
        rect = pygame.Rect(500, 500, 750, 500)
        rect.center = self.__center
        box = pygame.Surface((750, 500))
        opacity = 0.5
        pygame.Surface.fill(box, Color(0, 0, 0))
        box.set_alpha(math.floor(255 * opacity))
        if self.previous_game_state is not None:
            self.previous_game_state.render(0, graphics)
        graphics.draw_entity(Sprite(box), rect)
        for drawable in self.__scene:
            drawable.render(percentage, graphics)

    def handle_event_internal(self, event: Event):
        match event.name:
            case "pause" | "escape":
                self.go_previous_state()

    def on_update(self, lag):
        pass
