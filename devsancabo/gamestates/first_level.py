import decimal
import queue

from devsancabo.entities.player import Player
from devsancabo.internals import GameState


class FirstLevel(GameState):

    def __init__(self, events: queue.Queue, state_queue: queue.LifoQueue):
        super().__init__(events, state_queue)
        self.sceneTree = []
        self.player = Player()
        # add Background Entity to sceneTree
        # add Bounds Entity to sceneTree
        # Each entity sould have is_touching(other_entity)
        #                       is_inside(other_entity)
        # For this each entity should have a "collision box"
        # Each entity should have possibility of collision enabled or disabled
        # For example, "Background" has collision disabled
        self.sceneTree.append(self.player)
        self.redraw_background = True
        # camera object. it has a position and a rectangle attached(the viewport)
        # at the time of render. calculate objects within camera viewport
        # draw those objects, at positions relative to the camera(insted of world-cordinates)
        # add a thread that performs collision detection on a GameState.
        # on each collision, generate a CollisionEvent

    def handle_event_internal(self, event):
        print("handled event {0}".format(event))
        match event:
            case "move-down":
                # Delegate this command to entity
                # We shouldn't mess with the entity's internals
                self.player.move_down()
            case "stop-move-down":
                self.player.stop_move_down()
            case "stop-move-left":
                self.player.stop_move_left()
            case "stop-move-up":
                self.player.stop_move_up()
            case "stop-move-right":
                self.player.stop_move_right()
            case "move-up":
                self.player.move_up()
            case "move-left":
                self.player.move_left()
            case "move-right":
                self.player.move_right()
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
        if self.redraw_background:
            print("draw background")
            graphics.draw_background()
            self.redraw_background = False
        for e in self.sceneTree:
            e.render(percentage, graphics)
