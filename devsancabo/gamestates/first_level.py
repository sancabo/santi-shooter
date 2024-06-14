import asyncio
import math
import queue
import time
from threading import Thread

import pygame.display

from devsancabo.entities.background import Background
from devsancabo.entities.base import Drawable, Collisionable
from devsancabo.entities.bounds import Bounds
from devsancabo.entities.player import Player
from devsancabo.gamestates.timed_events import enemies_top, enemies_left, init_timed_events
from devsancabo.input import Event
from devsancabo.internals import GameState


class FirstLevel(GameState):

    def __init__(self, event_queue: queue.Queue, state_queue: queue.LifoQueue):
        super().__init__(event_queue, state_queue)
        self.sceneTree: [Drawable] = []
        self.player = Player(2000, 600)
        self.player.relocate_col_box(1440 // 2 - 100, 1020 // 2 - 100)
        self.__enemies = []
        self.background = Background()
        self.bounds = Bounds(0, 0, pygame.display.get_window_size()[0] - 160,
                             pygame.display.get_window_size()[1] - 160)
        self.sceneTree.append(self.background)
        self.sceneTree.append(self.player)
        self.sceneTree.append(self.bounds)
        # todo implement camera
        self.__enemies_spawned_top = 0
        self.__enemies_spawned_left = 0
        self.__collision_list = [self.player, self.bounds]
        init_timed_events(event_queue)

    def get_collision_entities(self) -> [Collisionable]:
        return self.__collision_list

    def on_update(self, lag):
        self.player.update_position(lag)
        for enemy in self.__enemies:
            enemy.update_position(lag)
        self.__generate_new_enemies()
        self.__resolve_collisions()

    def __generate_new_enemies(self):
        # todo : move this to "spawner" method
        if (self.__enemies_spawned_top < len(enemies_top) and
                self.elapsed_millis // 1000 > enemies_top[self.__enemies_spawned_top]):
            self.__spawn_enemy(True)
            self.__enemies_spawned_top = self.__enemies_spawned_top + 1

        if (self.__enemies_spawned_left < len(enemies_left) and
                self.elapsed_millis / 1000 > enemies_left[self.__enemies_spawned_left]):
            self.__spawn_enemy(False)
            self.__enemies_spawned_left = self.__enemies_spawned_left + 1

    def __resolve_collisions(self):
        # todo: implement collisions with enemies
        if not self.player.is_inside(self.bounds):
            self.relocate_out_of_bounds_player()

    def relocate_out_of_bounds_player(self):
        px, py, pw, ph = self.player.get_col_box()
        bx, by, bw, bh = self.bounds.get_col_box()
        if px < bx:
            self.player.move_col_box(bx - px + 1, 0)
        if px + pw > bx + bw:
            self.player.move_col_box(-px - pw + bx + bw - 1, 0)
        if py < by:
            self.player.move_col_box(0, by - py + 1)
        if py + ph > by + bh:
            self.player.move_col_box(0, -py - ph + by + bh - 1)

    def handle_event_internal(self, event: Event):
        # print("handled event {0}".format(event))
        self.events_handled = self.events_handled + 1
        match event.name:
            case "stop-move-down" | "stop-move-up":
                self.player.accelerate(y=0)
            case "stop-move-left" | "stop-move-right":
                self.player.accelerate(x=0)
            case "move-down":
                self.player.accelerate(y=2000)
            case "move-up":
                self.player.accelerate(y=-2000)
            case "move-left":
                self.player.accelerate(x=-2000)
            case "move-right":
                self.player.accelerate(x=2000)
            case "spawn_enemy_lineal_wave":
                if event.params[0] == "top":
                    thread = Thread(target=lineal_spawner, args=(2, event.params[1],))
                    thread.start()
            case "escape":
                self.finish()

    def render_internal(self, percentage, graphics):
        for entity in self.sceneTree:
            entity.render(percentage, graphics)

    def __spawn_enemy(self, enter_direction):
        if enter_direction:
            enemy_position = (50 + 50 * self.__enemies_spawned_top, -100)
        else:
            enemy_position = (-100, -50 + 50 * self.__enemies_spawned_top)

        enemy = Player(2000, 600)
        self.__enemies.append(enemy)

        if enter_direction:
            enemy.accelerate(y=2000)
        else:
            enemy.accelerate(x=2000)

        enemy.relocate_col_box(enemy_position[0], enemy_position[1])
        self.sceneTree.append(enemy)
        self.__collision_list.append(enemy)

        thread = Thread(target=self.__remove_enemy, args=(enemy,))
        thread.start()

    def __remove_enemy(self, enemy):
        time.sleep(10)
        self.__enemies.remove(enemy)


def lineal_spawner(delay, occurrences=1):
    start = time.time()
    spawned = 0
    while spawned < occurrences:
        elapsed = time.time() - start
        if elapsed >= delay:
            start = time.time()
            spawned = spawned + 1
            # todo: create enemy entities
            #print("SPAWN ENEMY " + spawned.__str__() + " " + occurrences.__str__())


def now():
    return math.floor(time.time() * 1000)
