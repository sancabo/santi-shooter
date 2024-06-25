grass = (14, 4)
pebble = (12, 1)
empty = (15, 0)
transparent = (0, 0)

cliff_1 = (2, 4)
cliff_2 = (3, 4)
cliff_3 = (2, 5)
cliff_4 = (3, 5)
cliff_5 = (2, 6)
cliff_6 = (3, 6)
cliff_7 = (1, 4)
cliff_8 = (2, 4)
cliff_9 = (1, 5)
cliff_10 = (2, 5)
cliff_11 = (1, 6)
cliff_12 = (2, 6)

bit_mappings = [grass, pebble, empty, transparent, cliff_1, cliff_2, cliff_3, cliff_4, cliff_5, cliff_6,
                cliff_7, cliff_8, cliff_9, cliff_10, cliff_11, cliff_12]


def get_filled_area(width: int, height: int, fill: int) -> [[int]]:
    return [[0 for i in range(width)] for j in range(height)]


class MultiPrimitive:
    def __init__(self, name: str, tile_matrix: [[int, int]]):
        if len(tile_matrix) == 0 or len(tile_matrix[0]) == 0:
            raise AttributeError("Multiprimitive must be at least 1x1 in size")
        else:
            self.dimensions = (len(tile_matrix[0]), len(tile_matrix))
            self.name = name
            self.matrix = tile_matrix


cliff = MultiPrimitive("Cliff", [[4, 5, 10, 11],
                                                [6, 7, 12, 13],
                                                [8, 9, 14, 15]])


def insert_in_area(area, offsets, multi_primitive: MultiPrimitive, pos):
    real_x = pos[0] - offsets[0]
    real_y = pos[1] - offsets[1]
    if 0 <= real_x + multi_primitive.dimensions[0] < len(area[0]):
        if 0 <= real_y + multi_primitive.dimensions[1] < len(area):
            for j in range(0, len(multi_primitive.matrix)):

                for i in range(0, len(multi_primitive.matrix[0])):
                    print("{0} - {1}".format(real_y + j, real_x + i))
                    area[real_y + j][real_x + i] = multi_primitive.matrix[j][i]
        else:
            raise AttributeError("Cannot insert Multiprimitive in area 1")
    else:
        raise AttributeError("Cannot insert Multiprimitive in area, in pos{0}".format(real_x + multi_primitive.dimensions[0]))
