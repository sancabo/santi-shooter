import pygame


class Graphics:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.background = pygame.image.load("assets/background.jpg").convert()
        self.player = pygame.image.load("assets/car_yellow.png").convert_alpha()
        fontObj1 = pygame.font.Font('freesansbold.ttf', 42)
        text_surface = fontObj1.render("Move around with WASD", True, Graphics.WHITE, Graphics.BLACK)
        text_surface_rect = text_surface.get_rect()
        text_surface_rect.center = (1280 // 2, 720 // 2)
        self.text_surface = text_surface
        self.text_rect = text_surface_rect

    def draw_background(self):
        print("{0}".format(self.background))
        self.screen.blit(self.background, (0, 0))

    def draw_entity(self, rectangle_entity, deltas):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.text_surface, self.text_rect)
        rectangle_entity = rectangle_entity.move(deltas[0], deltas[1])
        self.screen.blit(self.player, rectangle_entity)

    def print_screen(self):
        pygame.display.update()
