from abc import abstractmethod


class Collisionable:
    @abstractmethod
    def get_col_box(self) -> (int, int, int, int):
        pass

    @abstractmethod
    def move_col_box(self, x, y):
        pass

    def is_touching(self, other) -> bool:
        # print("is touching?")
        x1, y1, w1, h1 = self.get_col_box()
        x2, y2, w2, h2 = other.get_col_box()
        # if disjointed by x or disjointed by y -> are not touching
        return not (x1 + w1 < x2 or x1 > x2 + w2 or y1 > y2 + h2 or y1 + h1 < y2)

    def is_inside(self, other):
        x1, y1, w1, h1 = self.get_col_box()
        x2, y2, w2, h2 = other.get_col_box()

        return x2 < x1 and x1 + w1 < x2 + w2 and y2 < y1 and y1 + h1 < y2 + h2


class Moveable:
    # Moveable.apply_accel(accel, residual_lag)
    #   accel how much coord/second I want to modify the speed each second
    #   residual_lag value to add to #update_lag
    # Moveable.set_top_speed(top_speed)
    # Moveable.set_slippery_scale(slippery_scale)
    # Moveable(update_lag, slippery_scale = 1, top_speed = 1)
    #   update_lag used to scale speed and acceleration for calculation
    #   maximum coord/millisecond this entity can move
    #   slippery_scale how much of it's speed it loses each at stop, and each update
    pass


class GameEntity:
    def __init__(self, identifier: str, position: tuple[int, int] = (0, 0), drawable=None, father=None):
        self.__id = identifier
        self.__children: list[GameEntity] = []
        self.__father: GameEntity = father
        self.__child_position = position
        self.__drawable = drawable

    def get_id(self) -> str:
        return self.__id

    def set_drawable(self, drawable):
        self.__drawable = drawable

    def get_drawable(self):
        return self.__drawable

    def set_entity_position(self, x, y):
        self.__child_position = (x, y)

    def move_entity(self, deltas: (int, int)):
        self.__child_position = (self.__child_position[0] + deltas[0], self.__child_position[1] + deltas[1])

    def get_entity_position(self) -> tuple[int, int]:
        if self.__father is None:
            return self.__child_position
        else:
            return (self.__father.get_entity_position()[0] + self.__child_position[0],
                    self.__father.get_entity_position()[1] + self.__child_position[1])

    def get_children(self):
        return self.__children

    def get_child_by_id(self, identifier: str):
        result = []
        for child in self.__children:
            if child.get_id() == identifier:
                result.append(child)
        return result

    def get_child_by_id_deep(self, identifier: str):
        result = []
        for child in self.__children:
            if child.get_id() == identifier:
                result.append(child)
            result.append(child.get_child_by_id_deep(identifier))
        return result

    def __detach(self):
        self.__child_position = self.get_position()
        self.__father = None

    def detach_child_by_id(self, identifier: str):
        for child in self.__children:
            if child.get_id() == identifier:
                self.__children.remove(child)
                child.__detach()
