import time
from queue import Queue, LifoQueue
from threading import Thread

import pygame.display

from devsancabo.entities.UI import UserInterface
from devsancabo.entities.background import Background
from devsancabo.entities.base import Drawable
from devsancabo.entities.bounds import Bounds
from devsancabo.entities.damage_text import DamageText
from devsancabo.entities.enemy import Enemy
from devsancabo.entities.player import Player
from devsancabo.entities.spawner import LinealWaveEnemySpawner, RandomDirectionEnemySpawner
from devsancabo.entities.text import Text
from devsancabo.gamestates.pause import PauseMenu
from devsancabo.gamestates.timed_events import TimedEvents
from devsancabo.input import Event
from devsancabo.internals import GameState

GOLDEN_YELLOW_RGB = (255, 200, 100)

BLACK_RGB = (0, 0, 0)

CLEARED_MESSAGE = "Stage cleared! Press Esc to exit."


class FirstLevel(GameState):

    def __init__(self, event_queue: Queue, state_queue: LifoQueue):
        super().__init__(event_queue, state_queue)
        self.__sub_state = "normal"
        self.__updateables = []
        self.__state_queue = state_queue
        self.__event_queue = event_queue
        # V1.1 todo add 'layers' to scene tree
        self.__sceneTree: [Drawable] = []
        self.__damage_sound = pygame.mixer.Sound("assets/damage.mp3")
        self.__damage_sound.set_volume(0.2)
        self.__play_victory_music = 0
        pygame.mixer.music.load('assets/battle-theme.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.__player = Player(2000, 600, 750)
        self.__player.relocate_col_box(pygame.display.get_window_size()[0] // 2 - 100,
                                       pygame.display.get_window_size()[1] // 2 - 100)

        self.__enemies: [Enemy] = []

        self.__spawners: [LinealWaveEnemySpawner] = []

        self.__background = Background()

        self.__bounds = Bounds(0, 0, pygame.display.get_window_size()[0],
                               pygame.display.get_window_size()[1])

        self.__ui = UserInterface()
        self.__sceneTree.append(self.__background)
        self.__sceneTree.append(self.__player)
        self.__sceneTree.append(self.__bounds)
        # V1.1 todo implement camera
        self.__collision_list = [self.__player, self.__bounds]
        self.__updateables.append(self.__player)
        self.__timed_events = TimedEvents(event_queue)
        self.__updateables.append(self.__timed_events)

    def on_update(self, lag):
        for i, updatable in enumerate(self.__updateables.copy()):
            if updatable.is_done():
                self.__updateables.remove(updatable)

        for i, updatable in enumerate(self.__updateables):
            updatable.update_state(lag)

        for spawner in self.__spawners:
            for new_enemy in spawner.get_produced_enemies():
                self.__sceneTree.append(new_enemy)
                self.__updateables.append(new_enemy)
                self.__collision_list.append(new_enemy)
                self.__enemies.append(new_enemy)
        self.__clean_inactive_spawners()
        self.__resolve_collisions()
        if self.__player.is_dead():
            self.__event_queue.put(Event("player_died", []))
        if self.__play_victory_music == 1 and not pygame.mixer.music.get_busy():
            self.show_victory_screen()

    def show_victory_screen(self):
        self.__player.stop_sounds()
        pygame.mixer.music.load('assets/victory.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(1)
        bounds = pygame.Rect(self.__bounds.get_col_box())
        bounds = bounds.move(0, -bounds.height / 4)
        # V1.1 todo Encapsulate this in Text drawable
        outline_size_px = 4
        bounds = bounds.move(0, outline_size_px)
        bounds = bounds.move(outline_size_px, 0)
        self.__sceneTree.append(Text(CLEARED_MESSAGE, 75, bounds.center, BLACK_RGB))
        bounds = bounds.move(-2 * outline_size_px, 0)
        self.__sceneTree.append(Text(CLEARED_MESSAGE, 75, bounds.center, BLACK_RGB))
        bounds = bounds.move(0, -2 * outline_size_px)
        self.__sceneTree.append(Text(CLEARED_MESSAGE, 75, bounds.center, BLACK_RGB))
        bounds = bounds.move(2 * outline_size_px, 0)
        self.__sceneTree.append(Text(CLEARED_MESSAGE, 75, bounds.center, BLACK_RGB))
        bounds = bounds.move(-outline_size_px, 0)
        bounds = bounds.move(0, outline_size_px)
        self.__sceneTree.append(Text(CLEARED_MESSAGE, 75, bounds.center, GOLDEN_YELLOW_RGB))
        self.__updateables.clear()
        self.__play_victory_music = self.__play_victory_music + 1

    # V1.1 todo implement this as part of "updateable.is_done()" cycle
    # V1.05 bug: I can clear the stage at the same time as dying
    def __clean_inactive_spawners(self):
        for spawner in self.__spawners:
            if spawner.is_terminated():
                for enemy in spawner.get_total_produced_enemies():
                    self.__enemies.remove(enemy)
                    self.__updateables.remove(enemy)
                self.__spawners.remove(spawner)
                self.__updateables.remove(spawner)

    def __resolve_collisions(self):
        if not self.__player.is_inside(self.__bounds):
            self.relocate_out_of_bounds_player()
        for enemy in self.__enemies:
            if self.__player.is_touching(enemy):
                self.event_queue.put(Event("player_hurt"))

    #V1.1 todo Encapsulate in Player, by player.relocate*(x, y)
    def relocate_out_of_bounds_player(self):
        px, py, pw, ph = self.__player.get_col_box()
        bx, by, bw, bh = self.__bounds.get_col_box()
        if px < bx:
            self.__player.move_col_box(bx - px + 1, 0)
        if px + pw > bx + bw:
            self.__player.move_col_box(-px - pw + bx + bw - 1, 0)
        if py < by:
            self.__player.move_col_box(0, by - py + 1)
        if py + ph > by + bh:
            self.__player.move_col_box(0, -py - ph + by + bh - 1)

    def handle_event_internal(self, event: Event):
        # print("handled event {0}".format(event))
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
                    pygame.mixer.Sound.play(self.__damage_sound)
                    damage = 25
                    self.__player.hurt(damage)
                    self.__ui.drain_hp(damage / self.__player.get_max_hp())
                    text = DamageText(damage.__str__(),
                                      self.__player.get_col_box()[0] + self.__player.get_col_box()[2] / 2
                                      , self.__player.get_col_box()[1])
                    self.__sceneTree.append(text)
                    self.__updateables.append(text)
                    thread = Thread(target=self.__remove_entity, args=(text, 0.5,))
                    thread.start()
            case "stage_cleared":
                if self.__sub_state == "normal":
                    print("Stage cleared")
                    pygame.mixer.music.fadeout(7000)
                    self.__play_victory_music = 1
            case "pause":
                self.__player.stop_sounds()
                pause_sound = pygame.mixer.Sound("assets/pause.wav")
                pause_sound.set_volume(0.5)
                pause_sound.play(0)
                bounds = pygame.Rect(self.__bounds.get_col_box())
                self.__state_queue.put(PauseMenu(self.__event_queue, self.__state_queue, self, bounds.center))
            case "player_died":
                if self.__sub_state != "game_over":
                    self.__sub_state = "game_over"
                    self.__updateables.append(Gameover(self.__player, self.__sceneTree, self.__bounds))
                    # show Press R to Restart. Press Esc to leave
            case "escape":
                self.go_previous_state()

    def render_internal(self, percentage, graphics):
        for entity in self.__sceneTree:
            entity.render(percentage, graphics)
        self.__ui.render(percentage, graphics)

    def __remove_entity(self, entity, sleep_time):
        time.sleep(sleep_time)
        self.__sceneTree.remove(entity)
        self.__updateables.remove(entity)


class Gameover:
    def __init__(self, player, scene_tree, bounds):
        self.__elapsed = 0
        self.__done = False
        self.__player = player
        self.__scene_tree= scene_tree
        self.__bounds = bounds
        print("Game over.")
        pygame.mixer.music.fadeout(2000)
        self.__player.stop_sounds()
        self.__player.stop_movement()
        self.__player.disable_collision()
        sound = pygame.mixer.Sound("assets/catching-fire.mp3")
        sound.set_volume(0.5)
        sound.play(0)
        self.__player.kill()

    def update_state(self, lag):
        self.__elapsed = self.__elapsed + lag
        if self.__elapsed >= 2000 and not self.__done:
            sound = pygame.mixer.Sound("assets/game-over.wav")
            sound.set_volume(0.5)
            sound.play(0)
            bounds = pygame.Rect(self.__bounds.get_col_box())
            bounds = bounds.move(0, -bounds.height / 4)
            self.__scene_tree.append(Text("You died! Press Esc to leave", 60, bounds.center, GOLDEN_YELLOW_RGB))
            self.__done = True

    def is_done(self):
        return self.__done
