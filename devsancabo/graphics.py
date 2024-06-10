import pygame


class Graphics:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.screen.fill("black")

    def draw_circle(self, color, center, radius):
        pygame.draw.circle(self.screen, color, center, radius)

    def show(self):
        pygame.display.flip()
