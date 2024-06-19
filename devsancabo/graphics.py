import pygame


class Graphics:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))

    def draw_entity(self, sprite, rectangle_entity, area_of_sprite=None):
        if area_of_sprite is not None:
            self.screen.blit(sprite.get_image(), rectangle_entity, area_of_sprite)
        else:
            self.screen.blit(sprite.get_image(), rectangle_entity)

    def print_screen(self):
        pygame.display.update()


class Sprite:
    # Used in an attempt to encapsulate graphics implementation
    # In the future I'd like the game logic to be unaware of pygame
    # Implement various adapters for pygame.*****
    def __init__(self, surface):
        self.__surface = surface

    def get_image(self):
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

    def get_dimensions(self) -> (int, int):
        return self.__dimensions

    def render(self, percentage, graphics, sprite_sheet_box=None):
        graphics.draw_entity(
            self.sprite, pygame.Rect(self.__position[0],
                                     self.__position[1],
                                     self.__dimensions[0],
                                     self.__dimensions[1]),
            sprite_sheet_box)


class SceneTreeLayer:
    def __init__(self, next_layer=None):
        self.__next_layer: SceneTreeLayer = next_layer
        self.__this_layer: [Drawable] = []
        self.__groups_in_this_layer: [str] = []

    def add(self, entity: Drawable, z_index: int):
        if z_index > 0:
            if self.__next_layer is None:
                self.__next_layer = SceneTreeLayer()
            self.__next_layer.add(entity, z_index - 1)
        else:
            self.__this_layer.append(entity)

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

    def render(self, percentage, graphics, sprite_sheet_box=None):
        for entity in self.__this_layer:
            entity.render(percentage, graphics, sprite_sheet_box)
        if self.__next_layer is not None:
            self.__next_layer.render(percentage, graphics, sprite_sheet_box)
