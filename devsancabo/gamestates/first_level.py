import decimal
import queue

from devsancabo.entities.player import Player
from devsancabo.internals import GameState


class FirstLevel(GameState):

    def __init__(self, events: queue.Queue, state_queue: queue.LifoQueue):
        super().__init__(events, state_queue)
        self.sceneTree = []
        self.player = Player()
        self.sceneTree.append(self.player)

    def handle_event_internal(self, event):
        print("handled event {0}".format(event))
        match event:
            case "move-down":
                self.player.acceleration_y = 0.00007
            case "stop-move-down":
                self.player.acceleration_y = 0
            case "stop-move-left":
                self.player.acceleration_x = 0
            case "stop-move-up":
                self.player.acceleration_y = 0
            case "stop-move-right":
                self.player.acceleration_x = 0
            case "move-up":
                self.player.acceleration_y = -0.00007
            case "move-left":
                self.player.acceleration_x = -0.00007
            case "move-right":
                self.player.acceleration_x = 0.00007
            case "shoot":
                self.events_handled = self.events_handled + 1
            case "escape":
                self.events_handled = self.events_handled + 1
                self.state_queue.get_nowait()  # this means "go back to previous state"
                self.terminated = True
                print("handled event {0}".format(event))
            case _:
                print("cannot handle event {0}".format(event))

    def render_internal(self, percentage: decimal.Decimal, graphics):
        for e in self.sceneTree:
            e.render(percentage, graphics)
