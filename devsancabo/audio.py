import pygame


class Audio:
    def __init__(self):
        self.__volume = 1.0

    def set_volume(self, volume: float):
        self.__volume = volume

    def raise_volume(self, increment: float):
        self.__volume = self.__volume + increment

    def make_sound(self, path: str) -> pygame.mixer.Sound:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(self.__volume)
        return sound

    def play_sound(self, path: str, loops=0, override_volume=0) -> pygame.mixer.Sound:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(self.__volume + override_volume)
        sound.play(loops)
        return sound

    def play_music(self, path: str, loops=-1):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.__volume)
        pygame.mixer.music.play(loops)

    def get_gobal_volume(self) -> float:
        return self.__volume
