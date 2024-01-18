import pygame
from time import time


# класс музыкального проигрывателя
class SoundPlayer:
    def __init__(self):
        pygame.mixer.init()  # Инициализация mixer'а

    def play_sound(self, sound_file, sound_volume):
        sound = pygame.mixer.Sound(sound_file)  # Загрузка звукового файла
        sound.set_volume(sound_volume)  # Установка громкости
        sound.play()  # Проигрывание звука

    def play_music(self, music_file, sound_volume, repeat=True):
        pygame.mixer.music.load(music_file)  # Загрузка музыкального файла
        pygame.mixer.music.set_volume(sound_volume)
        pygame.mixer.music.play(-1 if repeat else 0)  # Проигрывание музыки с повтором (если указано)

    def pause_music(self):
        pygame.mixer.music.pause()  # Пауза музыки

    def unpause_music(self):
        pygame.mixer.music.unpause()  # Возобновление проигрывания музыки

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)


def render_of_text(screen, text, rect_center, size=80, color='gray'):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect_center)
    screen.blit(text_surface, text_rect)


# класс секундомера
class Stopwatch:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0

    def start(self):
        self.start_time = time()

    def stop(self):
        self.end_time = time()

    def elapsed_time(self):
        return self.end_time - self.start_time

    def reset(self):
        self.__init__()


def transform_time(seconds):
    hours, minutes, seconds = 0, 0, seconds

    while seconds >= 60 or minutes >= 60:
        if seconds >= 60:
            minutes += 1
            seconds -= 60
        if minutes >= 60:
            hours += 1
            minutes -= 60

    return hours, minutes, seconds
