import math
import math
import queue
import time
from threading import Thread

import pygame.display

from devsancabo.entities.UI import UserInterface
from devsancabo.entities.background import Background
from devsancabo.entities.base import Drawable, Collisionable
from devsancabo.entities.bounds import Bounds
from devsancabo.entities.damage_text import DamageText
from devsancabo.entities.enemy import Enemy
from devsancabo.entities.player import Player
from devsancabo.entities.spawner import EnemySpawner
from devsancabo.gamestates.timed_events import init_timed_events
from devsancabo.input import Event
from devsancabo.internals import GameState


class FirstLevel(GameState):

    def __init__(self, event_queue: queue.Queue, state_queue: queue.LifoQueue):
        super().__init__(event_queue, state_queue)
        self.__updateables = []
        self.__sceneTree: [Drawable] = []
        self.__damage_sound = pygame.mixer.Sound("assets/damage.mp3")
        self.__damage_sound.set_volume(0.2)
        pygame.mixer.music.load('assets/battle-theme.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        #(3)todo: player (and other entities) should have only one position, which is used by render and colision
        self.__player = Player(2000, 600)
        self.__player.relocate_col_box(1440 // 2 - 100, 1020 // 2 - 100)

        self.__enemies : [Enemy] = []

        self.__spawners : [EnemySpawner] = []

        self.__background = Background()

        self.__bounds = Bounds(0, 0, pygame.display.get_window_size()[0],
                               pygame.display.get_window_size()[1])

        self.__ui = UserInterface()
        self.__sceneTree.append(self.__background)
        self.__sceneTree.append(self.__player)
        self.__sceneTree.append(self.__bounds)
        # todo implement camera
        self.__collision_list = [self.__player, self.__bounds]
        self.__updateables.append(self.__player)
        init_timed_events(event_queue)

    def get_collision_entities(self) -> [Collisionable]:
        return self.__collision_list

    def on_update(self, lag):
        for i, updatable in enumerate(self.__updateables):
            updatable.update_state(lag)
        for spawner in self.__spawners:
            for new_enemy in spawner.get_produced_enemies():
                self.__sceneTree.append(new_enemy)
                self.__updateables.append(new_enemy)
                self.__collision_list.append(new_enemy)
                self.__enemies.append(new_enemy)
        self.__clean_spawners()
        self.__resolve_collisions()

    def __clean_spawners(self):
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

    #(3)todo: shouldn't move colision box manually. It should update with player position
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
                self.__player.accelerate(y=0)
            case "stop-move-left" | "stop-move-right":
                self.__player.accelerate(x=0)
            case "move-down":
                self.__player.accelerate(y=2000)
            case "move-up":
                self.__player.accelerate(y=-2000)
            case "move-left":
                self.__player.accelerate(x=-2000)
            case "move-right":
                self.__player.accelerate(x=2000)
            case "spawn_enemy_lineal_wave":
                print("spawn enemy lineal wave")
                spawner = EnemySpawner(1, event.params[0], self.__bounds, event.params[1])
                self.__spawners.append(spawner)
                self.__updateables.append(spawner)
            case "player_hurt":
                if self.__player.is_vulnerable():
                    pygame.mixer.Sound.play(self.__damage_sound)
                    self.__player.hurt(25)
                    self.__ui.drain_hp(25 / 500)
                    text = DamageText("25", self.__player.get_col_box()[0] + self.__player.get_col_box()[2] / 2
                                      , self.__player.get_col_box()[1])
                    self.__sceneTree.append(text)
                    self.__updateables.append(text)
                    thread = Thread(target=self.__remove_entity, args=(text, 0.5,))
                    thread.start()
            case "escape":
                self.finish()

    def render_internal(self, percentage, graphics):
        for entity in self.__sceneTree:
            entity.render(percentage, graphics)
        self.__ui.render(percentage, graphics)

    def __remove_enemy(self, enemy):
        time.sleep(10)
        self.__enemies.remove(enemy)
        self.__sceneTree.remove(enemy)

    def __remove_entity(self, entity, sleep_time):
        time.sleep(sleep_time)
        self.__sceneTree.remove(entity)
        self.__updateables.remove(entity)


def now():
    return math.floor(time.time() * 1000)
