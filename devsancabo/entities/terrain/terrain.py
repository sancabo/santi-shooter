import pygame.image

from devsancabo.entities.base import GameEntity
from devsancabo.entities.camera import Camera
from devsancabo.entities.terrain.tileset import bit_mappings, get_filled_area, cliff, insert_in_area
from devsancabo.graphics import Sprite, Drawable

grass = (14, 4)
pebble = (12, 1)
empty = (15, 0)
transparent = (0, 0)


# 16*16 tiles. tile: 32x32
class Terrain(GameEntity):
    def __init__(self, viewport: (int, int, int, int)):
        super().__init__("terrain")
        self.set_entity_position(viewport[0], viewport[1])
        # -50_000, -50_000, 100_000, 100_000
        self.__sprite_sheet = pygame.image.load("assets/mountain_landscape.png").convert_alpha()
        self.__tile_size = 32
        self.__tile_per_row = 16
        self.__mappings = [(14, 4), (12, 1), (15, 0)]
        self.__map_dimensions = (1000, 1000)
        self.__map = get_filled_area(self.__map_dimensions[0], self.__map_dimensions[1], 0)
        self.drawable = Drawable(Sprite(self.__sprite_sheet), 0, 0, viewport[2], viewport[3])

        for i in range(0,  self.__map_dimensions[0] - 4, 4):
            insert_in_area(self.__map, self.get_entity_position(), cliff, (i, -3))

    def render(self, percentage, graphics, camera: Camera, box=None):
        camera_width = camera.get_bounds().width
        camera_height = camera.get_bounds().height

        tile_x = (camera.get_bounds().left - self.get_entity_position()[0]) // 32
        last_tile_x = tile_x + (camera_width // 32) + 1
        offset_x = camera.get_bounds().left % 32
        tile_y = (camera.get_bounds().top - self.get_entity_position()[1]) // 32
        last_tile_y = tile_y + (camera_height // 32) + 1
        offset_y = camera.get_bounds().top % 32
        # print("{0} - {1} - {2} - {3}".format(tile_x, tile_y, last_tile_x, last_tile_y))

        frame = pygame.surface.Surface((camera_width, camera_height))
        for i in range(tile_x, last_tile_x):
            for j in range(tile_y, last_tile_y):

                rel_y = j - tile_y
                rel_x = i - tile_x
                if 0 <= j < self.__map_dimensions[1] and 0 <= i < self.__map_dimensions[0]:

                    frame.blit(self.__sprite_sheet, ((rel_x * 32) - offset_x, (rel_y * 32) - offset_y),
                               pygame.Rect(bit_mappings[self.__map[j][i]][0] * 32,
                                           bit_mappings[self.__map[j][i]][1] * 32, 32, 32))
                    # print("will print {0}".format(pygame.Rect(bit_mappings[self.__map[j][i]][0] * 32,
                   #                                           bit_mappings[self.__map[j][i]][1] * 32, 32, 32)))
                else:
                    frame.blit(self.__sprite_sheet, ((rel_x * 32) - offset_x, (rel_y * 32) - offset_y),
                               pygame.Rect(bit_mappings[0][0] * 32,
                                           bit_mappings[0][1] * 32, 32, 32))
        self.drawable.set_image(Sprite(frame))
        self.drawable.set_position(camera.get_entity_position()[0], camera.get_entity_position()[1])
        self.drawable.render(percentage, graphics, camera)
