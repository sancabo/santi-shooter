from queue import Queue, LifoQueue

import pygame.display

from devsancabo.audio import Audio
from devsancabo.entities.UI import UserInterface
from devsancabo.entities.background import Background
from devsancabo.entities.bounds import Bounds
from devsancabo.entities.camera import Camera
from devsancabo.entities.damage_text import DamageText
from devsancabo.entities.player import Player
from devsancabo.entities.projectile.projectile import Projectile
from devsancabo.entities.projectile.shot_2 import Shot
from devsancabo.entities.spawner import LinealWaveEnemySpawner, RandomDirectionEnemySpawner
from devsancabo.entities.text import Text
from devsancabo.gamestates.base_game_states import GameState
from devsancabo.gamestates.gameover import Gameover
from devsancabo.gamestates.pause import PauseMenu
from devsancabo.gamestates.timed_events import TimedEvents
from devsancabo.graphics import SceneTreeLayer
from devsancabo.input import Event

GOLDEN_YELLOW_RGB = (255, 200, 100)

BLACK_RGB = (0, 0, 0)

CLEARED_MESSAGE = "Stage cleared! Press Esc to exit."


class FirstLevel(GameState):

    def __init__(self, event_queue: Queue, state_queue: LifoQueue, audio: Audio, viewport: tuple[int, int]):
        super().__init__(event_queue, state_queue, audio)
        self.__audio = audio
        self.__sub_state = "normal"
        self.__updateables = []
        self.__state_queue = state_queue
        self.__event_queue = event_queue
        self.__scene_tree: SceneTreeLayer = SceneTreeLayer()
        self.__play_victory_music = 0
        self.__audio.play_music('assets/battle-theme.mp3')
        self.__player = Player(self.__audio, 2000, 600, 100)
        self.__player.relocate_col_box(pygame.display.get_window_size()[0] // 2 - 100,
                                       pygame.display.get_window_size()[1] // 2 - 100)

        self.__enemies: [Projectile] = []
        self.__shots: [Shot] = []
        self.__spawners: [LinealWaveEnemySpawner] = []
        self.__background = Background()
        self.__bounds = Bounds(0, 0, pygame.display.get_window_size()[0],
                               pygame.display.get_window_size()[1])
        self.__ui = UserInterface()
        self.__scene_tree.add(self.__background)
        self.__scene_tree.add(self.__player, 3)
        self.__scene_tree.add(self.__bounds)
        self.__scene_tree.add(self.__ui)

        self.__updateables.append(self.__player)
        self.__timed_events = TimedEvents(event_queue)
        self.__updateables.append(self.__timed_events)

        self.__viewport = viewport
        self.__camera = Camera((0, 0, viewport[0], viewport[1]), "camera-01")

    def on_update(self, lag):
        for i, updatable in enumerate(self.__updateables.copy()):
            if updatable.is_done():
                try:
                    self.__scene_tree.remove(updatable)
                    self.__updateables.remove(updatable)
                    self.__enemies.remove(updatable)
                    self.__spawners.remove(updatable)
                except ValueError:
                    pass

        for i, updatable in enumerate(self.__updateables):
            updatable.update_state(lag)

        for spawner in self.__spawners.copy():
            for new_enemy in spawner.get_produced_enemies():
                self.__scene_tree.add(new_enemy, 1)
                self.__updateables.append(new_enemy)
                self.__enemies.append(new_enemy)

        self.__resolve_collisions()
        if self.__player.is_dead():
            self.__event_queue.put(Event("player_died", []))
        if self.__play_victory_music == 1 and not pygame.mixer.music.get_busy():
            self.show_victory_screen()
        self.__camera.move_entity((1, 0))

    def show_victory_screen(self):
        self.__player.stop_sounds()
        self.__audio.play_music('assets/victory.wav', 0)
        bounds = pygame.Rect(self.__bounds.get_col_box())
        bounds = bounds.move(0, -bounds.height / 4)
        self.__scene_tree.add(Text(CLEARED_MESSAGE, 75, bounds.center, GOLDEN_YELLOW_RGB, (4, BLACK_RGB)), 10)
        self.__updateables.clear()
        self.__play_victory_music = self.__play_victory_music + 1

    def __resolve_collisions(self):
        if not self.__player.is_inside(self.__bounds):
            self.__player.relocate_in_bounds(self.__bounds)
        for enemy in self.__enemies:
            if self.__player.is_touching(enemy):
                self.event_queue.put(Event("player_hurt"))

    def handle_event_internal(self, event: Event):
        self.events_handled = self.events_handled + 1
        match event.name:
            case "stop-move-down" | "stop-move-up":
                if self.__sub_state == "normal":
                    self.__player.accelerate(y=0)
            case "stop-move-left" | "stop-move-right":
                if self.__sub_state == "normal":
                    self.__player.accelerate(x=0)
            case "move-down":
                if self.__sub_state == "normal":
                    self.__player.accelerate(y=2000)
            case "move-up":
                if self.__sub_state == "normal":
                    self.__player.accelerate(y=-2000)
            case "move-left":
                if self.__sub_state == "normal":
                    self.__player.accelerate(x=-2000)
            case "move-right":
                if self.__sub_state == "normal":
                    self.__player.accelerate(x=2000)
            case "shoot":
                if self.__sub_state == "normal":
                    # todo encapsulate shooting weapon on player
                    shot = Shot(self.__player.get_center(), 750)
                    shot.set_speed_vector(self.__player.get_speed_vector(), 1300)
                    self.__scene_tree.add(shot, 1)
                    self.__updateables.append(shot)
                    self.__shots.append(shot)
            case "spawn_enemy_lineal_wave":
                print("spawn enemy lineal wave")
                spawner = LinealWaveEnemySpawner(1, event.params[0], self.__bounds, event.params[1])
                self.__spawners.append(spawner)
                self.__updateables.append(spawner)
            case "spawn_enemy_random_direction":
                print("spawn enemy random direction")
                spawner = RandomDirectionEnemySpawner(self.__bounds, self.__player, event.params[0], event.params[1])
                self.__spawners.append(spawner)
                self.__updateables.append(spawner)
            case "player_hurt":
                if self.__player.is_vulnerable():
                    self.__audio.play_sound("assets/damage.mp3")
                    damage = 25
                    self.__player.hurt(damage)
                    self.__ui.drain_hp(damage / self.__player.get_max_hp())
                    text = DamageText(damage.__str__(),
                                      self.__player.get_col_box()[0] + self.__player.get_col_box()[2] / 2
                                      , self.__player.get_col_box()[1])
                    self.__scene_tree.add(text, 2)
                    self.__updateables.append(text)
            case "stage_cleared":
                if self.__sub_state == "normal":
                    print("Stage cleared")
                    pygame.mixer.music.fadeout(7000)
                    self.__play_victory_music = 1
            case "pause":
                if self.__sub_state == "normal":
                    self.__player.stop_sounds()
                    self.__audio.play_sound("assets/pause.wav")
                    bounds = pygame.Rect(self.__bounds.get_col_box())
                    self.__state_queue.put(PauseMenu(self.__event_queue,
                                                     self.__state_queue,
                                                     self.__audio,
                                                     self.__scene_tree,
                                                     self,
                                                     bounds.center, self))
            case "player_died":
                if self.__sub_state != "game_over":
                    self.__sub_state = "game_over"
                    self.__state_queue.put(Gameover(self.__event_queue,
                                                    self.__state_queue,
                                                    self.__audio,
                                                    self.__player,
                                                    self,
                                                    self.__bounds.get_col_box()))
                    # show Press R to Restart. Press Esc to leave
            case "escape":
                self.go_previous_state()
            case "restart":
                if self.__sub_state == "game_over":
                    self.go_previous_state()
                    self.go_to_state(FirstLevel(self.event_queue, self.state_queue, self.__audio, self.__viewport))

    def render_internal(self, percentage, graphics):
        self.__scene_tree.render(percentage, graphics, self.__camera)
