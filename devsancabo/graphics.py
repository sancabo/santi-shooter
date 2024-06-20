import pygame

from devsancabo.entities.camera import Camera


class Graphics:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self, w, h, fullscreen=True):
        pygame.init()
        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((w, h))

    def reset_display(self, w, h, fullscreen):
        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((w, h))

    def draw_entity(self, sprite, rectangle_entity, area_of_sprite=None):
        if area_of_sprite is not None:
            self.screen.blit(sprite.get_image(), rectangle_entity, area_of_sprite)
        else:
            self.screen.blit(sprite.get_image(), rectangle_entity)

    def print_screen(self):
        pygame.display.update()

    def get_window_size(self) -> tuple[int, int]:
        return pygame.display.get_window_size()


class Sprite:
    # add method to handle animated sprites
    def __init__(self, surface):
        self.__surface = surface

    def get_image(self) -> pygame.Surface:
        return self.__surface


class Drawable:

    def __init__(self, sprite: Sprite, x=0, y=0, width=0, height=0):
        self.sprite = sprite
        self.__position = (x, y)
        self.__dimensions = (width, height)

    def set_image(self, sprite: Sprite):
        self.sprite = sprite

    def set_position(self, x, y):
        self.__position = (x, y)

    def get_position(self) -> (int, int):
        return self.__position

    def set_dimensions(self, dim: (int, int)):
        self.__dimensions = dim

    def get_dimensions(self) -> (int, int):
        return self.__dimensions

    def render(self, percentage, graphics, camera: Camera = None, sprite_sheet_box=None):
        if camera is None:
            graphics.draw_entity(self.sprite, pygame.Rect(self.__position[0],
                                                          self.__position[1],
                                                          self.__dimensions[0],
                                                          self.__dimensions[1]), sprite_sheet_box)
        else:
            if camera.is_touching(self.__position[0], self.__position[1], self.__dimensions[0], self.__dimensions[1]):
                relative_pos = (self.__position[0] - camera.get_entity_position()[0],
                                self.__position[1] - camera.get_entity_position()[1])
                graphics.draw_entity(self.sprite, pygame.Rect(relative_pos[0],
                                                              relative_pos[1],
                                                              self.__dimensions[0],
                                                              self.__dimensions[1]), sprite_sheet_box)


class SceneTreeLayer:
    def __init__(self, next_layer=None):
        self.__next_layer: SceneTreeLayer = next_layer
        self.__this_layer: [Drawable] = []
        self.__groups_in_this_layer: [str] = []

    def add(self, entity: Drawable, z_index: int = 0):
        if z_index > 0:
            if self.__next_layer is None:
                self.__next_layer = SceneTreeLayer()
            self.__next_layer.add(entity, z_index - 1)
        else:
            self.__this_layer.append(entity)

    def remove(self, entity: Drawable):
        if entity not in self.__this_layer:
            if self.__next_layer is not None:
                self.__next_layer.remove(entity)
        else:
            self.__this_layer.remove(entity)

    def create_group(self, name: str, z_index: int):
        if z_index > 0:
            if self.__next_layer is None:
                self.__next_layer = SceneTreeLayer()
            self.__next_layer.create_group(name, z_index - 1)
        else:
            self.__groups_in_this_layer.append(name)

    def add_to_group(self, entity: Drawable, name: str):
        if name not in self.__groups_in_this_layer:
            if self.__next_layer is not None:
                self.__next_layer.add_to_group(entity, name)
        else:
            self.__this_layer.append(entity)

    def insert_entities_at(self, entities: [Drawable], z_index: int = 0):
        # insert entities at z_index
        # if layer wasn't empty, move current and all sub layers one z level higher
        pass

    def insert_group_at(self, entity: Drawable, z_index: int = 0):
        # create empty group at z_index
        # if layer wasn't empty, move current and all sub layers one z level higher
        pass

    def get_z_index_of_entity(self, entity: Drawable) -> int:
        # implement later
        pass

    def get_z_index_of_group(self, group: str) -> int:
        # implement later
        pass

    def render(self, percentage, graphics, camera: Camera = None, sprite_sheet_box=None):
        for entity in self.__this_layer:
            entity.render(percentage, graphics, camera, sprite_sheet_box)
        if self.__next_layer is not None:
            self.__next_layer.render(percentage, graphics, camera, sprite_sheet_box)

    def remove_group(self, name):
        if name not in self.__groups_in_this_layer:
            if self.__next_layer is not None:
                self.__next_layer.remove_group(name)
        else:
            self.__this_layer.clear()
