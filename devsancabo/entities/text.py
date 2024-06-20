import pygame

from devsancabo.graphics import Sprite, Drawable

BLACK_RGB = (0, 0, 0)


class Text(Drawable):

    def __init__(self, text: str,
                 size: int,
                 center: (int, int) = (0, 0),
                 color: (int, int, int) = (255, 255, 255),
                 outline: (int, (int, int, int)) = (0, BLACK_RGB)):
        self.__outlines: [Drawable] = []
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(text, True, color)
        self.__text = Sprite(text_surface)
        text_surface_rect = self.__text.get_image().get_rect()
        text_surface_rect.center = center
        super().__init__(self.__text, text_surface_rect.left, text_surface_rect.top,
                         text_surface_rect.width, text_surface_rect.height)

        if outline[0] > 0:
            text_surface = font.render(text, True, outline[1])
            self.__text = Sprite(text_surface)

            new_center = (text_surface_rect.center[0] + outline[0],
                          text_surface_rect.center[1] + outline[0])
            text_surface_rect = text_surface_rect.copy()
            text_surface_rect.center = new_center
            self.__outlines.append(Drawable(self.__text, text_surface_rect.left, text_surface_rect.top,
                                            text_surface_rect.width, text_surface_rect.height))

            new_center = (text_surface_rect.center[0] - 2 * outline[0],
                          text_surface_rect.center[1] + 0)
            text_surface_rect = text_surface_rect.copy()
            text_surface_rect.center = new_center
            self.__outlines.append(Drawable(self.__text, text_surface_rect.left, text_surface_rect.top,
                                            text_surface_rect.width, text_surface_rect.height))

            new_center = (text_surface_rect.center[0] + 0,
                          text_surface_rect.center[1] - 2 * outline[0])
            text_surface_rect = text_surface_rect.copy()
            text_surface_rect.center = new_center
            self.__outlines.append(Drawable(self.__text, text_surface_rect.left, text_surface_rect.top,
                                            text_surface_rect.width, text_surface_rect.height))

            new_center = (text_surface_rect.center[0] + 2 * outline[0],
                          text_surface_rect.center[1] + 0)
            text_surface_rect = text_surface_rect.copy()
            text_surface_rect.center = new_center
            self.__outlines.append(Drawable(self.__text, text_surface_rect.left, text_surface_rect.top,
                                            text_surface_rect.width, text_surface_rect.height))

    def render(self, percentage, graphics, camera, sprite_sheet_box=None):
        for outline in self.__outlines:
            outline.render(percentage, graphics, camera)

        super().render(percentage, graphics, camera)