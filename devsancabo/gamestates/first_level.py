import queue

import pygame.display

from devsancabo.entities.background import Background
from devsancabo.entities.base import Drawable, Collisionable
from devsancabo.entities.bounds import Bounds
from devsancabo.entities.player import Player
from devsancabo.gamestates.first_level_events import enemies
from devsancabo.internals import GameState


class FirstLevel(GameState):

    def __init__(self, events: queue.Queue, state_queue: queue.LifoQueue):
        super().__init__(events, state_queue)
        self.__direction = 0
        self.sceneTree: [Drawable] = []
        self.player = Player(2000, 600)
        self.__enemies = []
        self.background = Background()
        self.bounds = Bounds(0, 0, pygame.display.get_window_size()[0] - 160,
                             pygame.display.get_window_size()[1] - 160)
        # Each entity should have possibility of collision enabled or disabled
        # For example, "Background" has collision disabled
        self.sceneTree.append(self.background)
        self.sceneTree.append(self.player)
        self.sceneTree.append(self.bounds)
        # camera object. it has a position and a rectangle attached(the viewport)
        # at the time of render. calculate objects within camera viewport
        # draw those objects, at positions relative to the camera(insted of world-cordinates)
        # add a thread that performs collision detection on a GameState.
        # on each collision, generate a CollisionEvent
        self.__enemies_spawned = 0
        self.__collision_list = [self.player, self.bounds]

    def get_collision_entities(self) -> [Collisionable]:
        return self.__collision_list

    def on_update(self, lag):
        self.player.update_position(lag)
        for enemy in self.__enemies:
            enemy.update_position(lag)
        if self.__enemies_spawned < 5 and self.elapsed_millis//1000 > enemies[self.__enemies_spawned]:
            self.__spawn_enemy()
            self.__enemies_spawned = self.__enemies_spawned + 1
        if not self.player.is_inside(self.bounds):
            self.relocate_out_of_bounds_player()
        #for i, ci in enumerate(self.__collision_list, 0):
            #for j, cj in enumerate(self.__collision_list, 0):
                #if i != j and not ci.is_inside(cj):
                    #out_of_bounds = out_of_bounds + 1


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

    def handle_event_internal(self, event):
        # print("handled event {0}".format(event))
        self.events_handled = self.events_handled + 1
        match event:
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
            case "out-of-bounds":
                # Move player inside the bounds in the shortest distance possible
                pass
            case "escape":
                self.__state_queue.get_nowait()  # this means "go back to previous state"
                self.terminated = True

    def render_internal(self, percentage, graphics):
        for entity in self.sceneTree:
            entity.render(percentage, graphics)

    def __spawn_enemy(self):
        enemy_position = (100 + 100*self.__enemies_spawned, 100 + 100*self.__enemies_spawned)
        enemy = Player(2000, 600)
        self.__enemies.append(enemy)
        xa = [2000, -2000, 0, 0]
        ya = [0, 0, 2000, -2000]
        enemy.accelerate(x=xa[self.__direction ], y=ya[self.__direction ])
        enemy.relocate_col_box(enemy_position[0], enemy_position[1])
        self.sceneTree.append(enemy)
        self.__collision_list.append(enemy)
        self.__direction = (self.__direction + 1) % 4

