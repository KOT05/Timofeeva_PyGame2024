import pygame


# класс кнопки
class Button:
    def __init__(self, text, position, width, height, color, hover_color, text_color, font_size):
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color  # Цвет при наведении
        self.text_color = text_color
        self.font_size = font_size  # Размер шрифта
        self.font = pygame.font.Font(None, self.font_size)  # шрифт по умолчанию указанного размера
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        self.hovered = False

    def draw(self, screen):
        if self.is_hovered(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self, mouse_pos):  # проверка наведения мыши на кнопку
        if self.rect.collidepoint(mouse_pos):
            return True
        return False


# класс музыкального проигрывателя
class SoundPlayer:
    def __init__(self):
        pygame.mixer.init()  # Инициализация mixer'а

    def play_sound(self, sound_file, volume=0.1):
        sound = pygame.mixer.Sound(sound_file)  # Загрузка звукового файла
        sound.set_volume(volume)  # Установка громкости
        sound.play()  # Проигрывание звука

    def play_music(self, music_file, repeat=True):
        pygame.mixer.music.load(music_file)  # Загрузка музыкального файла
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1 if repeat else 0)  # Проигрывание музыки с повтором (если указано)

    def pause_music(self):
        pygame.mixer.music.pause()  # Пауза музыки

    def unpause_music(self):
        pygame.mixer.music.unpause()  # Возобновление проигрывания музыки

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)


def rendering(screen, text, way_to_picture, picture_size, rect_center):
    screen.fill((0, 0, 0))
    main_background = pygame.image.load(way_to_picture)
    main_background = pygame.transform.scale(main_background, picture_size)
    screen.blit(main_background, (0, 0))

    font = pygame.font.Font(None, 80)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect_center)
    screen.blit(text_surface, text_rect)
