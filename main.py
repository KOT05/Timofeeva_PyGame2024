import pygame
import ctypes
import sys
from level import Level
from level_data import all_levels
from functions import Button, rendering, SoundPlayer

WIDTH, HEIGHT = 1920, 1080
SOUND_VOLUME = 0.25


def game_start(level_ind):
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    clock = pygame.time.Clock()

    # выбор уровня
    level = Level(all_levels[level_ind], screen)

    running = True
    while running:
        # выход
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # если нажали esc, возвращаемся к главному окну
                if event.key == pygame.K_ESCAPE:

                    running = False
                    choose_level()
                # если нажали r, то уровень начинается заново
                elif event.key == pygame.K_r:
                    level = Level(all_levels[level_ind], screen)
            # проверка кнопки restart на экране
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for sprite in level.button_sprites.sprites():
                    # еслт координаты курсора совпадают с кнопкой, то уровень начинается заново
                    if sprite.rect.colliderect(mouse_pos[0], mouse_pos[1], 1, 1):
                        level = Level(all_levels[level_ind], screen)

        screen.fill((6, 5, 13))

        # переход к другому уровню
        if level.should_change:
            level_ind += 1
            level = Level(all_levels[level_ind], screen)

            level.should_change = False

        # проверка смерти
        if level.should_restart:
            level = Level(all_levels[level_ind], screen)
            level.should_restart = False

        # запуск уровня
        level.run()

        pygame.display.update()
        clock.tick(60)


def main_menu(screen):
    pygame.display.set_mode((640, 480))
    start_button = Button('Играть', (250, 150), 150, 50, 'green', 'red', 'purple', 40)
    settings_button = Button('Настройки', (250, 210), 150, 50, 'green', 'red', 'purple', 40)
    exit_button = Button('Выход', (250, 270), 150, 50, 'green', 'red', 'purple', 40)

    running = True
    while running:
        # отрисовка основных элементов на экране
        rendering(screen, 'Побег', r'Resources\Images\dream_TradingCard.jpg', (640, 480), (320, 100))

        start_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_hovered(event.pos):
                    choose_level()
                elif exit_button.is_hovered(event.pos):
                    sys.exit()
                elif settings_button.is_hovered(event.pos):
                    settings_menu(screen)

        pygame.display.update()


def settings_menu(screen):
    audio_button = Button('Звук', (250, 150), 150, 50, 'green', 'red', 'purple', 40)
    video_button = Button('Видео', (250, 210), 150, 50, 'green', 'red', 'purple', 40)
    exit_button = Button('Выход', (250, 270), 150, 50, 'green', 'red', 'purple', 40)

    running = True
    while running:
        rendering(screen, 'Настройки', r'Resources\Images\dream_TradingCard.jpg', (640, 480), (320, 100))

        audio_button.draw(screen)
        video_button.draw(screen)
        exit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if audio_button.is_hovered(event.pos):
                    audio_settings(screen)
                elif video_button.is_hovered(event.pos):
                    video_settings(screen)
                elif exit_button.is_hovered(event.pos):
                    running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame.display.update()


def video_settings(screen):
    global WIDTH, HEIGHT
    resolution_button_1 = Button('800x600', (250, 150), 150, 50, 'green', 'red', 'purple', 40)
    resolution_button_2 = Button('1280x720', (250, 210), 150, 50, 'green', 'red', 'purple', 40)
    resolution_button_3 = Button('1920x1080', (250, 270), 150, 50, 'green', 'red', 'purple', 40)
    exit_button = Button('Выход', (250, 330), 150, 50, 'green', 'red', 'purple', 40)

    running = True
    while running:
        rendering(screen, 'Разрешение экрана', r'Resources\Images\dream_TradingCard.jpg', (640, 480), (320, 100))

        resolution_button_1.draw(screen)
        resolution_button_2.draw(screen)
        resolution_button_3.draw(screen)
        exit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.is_hovered(event.pos):
                    running = False
                elif resolution_button_1.is_hovered(event.pos):
                    WIDTH, HEIGHT = 800, 600
                elif resolution_button_2.is_hovered(event.pos):
                    WIDTH, HEIGHT = 1280, 720
                elif resolution_button_3.is_hovered(event.pos):
                    WIDTH, HEIGHT = 1920, 1080
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame.display.update()


def audio_settings(screen):
    global SOUND_VOLUME

    volume_1 = Button('100%', (250, 150), 150, 50, 'green', 'red', 'purple', 40)
    volume_2 = Button('50%', (250, 210), 150, 50, 'green', 'red', 'purple', 40)
    volume_3 = Button('25%', (250, 270), 150, 50, 'green', 'red', 'purple', 40)
    volume_4 = Button('on/off', (250, 330), 150, 50, 'green', 'red', 'purple', 40)
    exit_button = Button('Выход', (250, 390), 150, 50, 'green', 'red', 'purple', 40)

    running = True
    while running:
        rendering(screen, 'Настройки звука', r'Resources\Images\dream_TradingCard.jpg', (640, 480), (320, 100))

        volume_1.draw(screen)
        volume_2.draw(screen)
        volume_3.draw(screen)
        volume_4.draw(screen)
        exit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.is_hovered(event.pos):
                    running = False
                else:
                    if volume_1.is_hovered(event.pos):
                        SOUND_VOLUME = 1
                    elif volume_2.is_hovered(event.pos):
                        SOUND_VOLUME = 0.5
                    elif volume_3.is_hovered(event.pos):
                        SOUND_VOLUME = 0.25
                    elif volume_4.is_hovered(event.pos):
                        SOUND_VOLUME = 0
                    Music_player.set_volume(SOUND_VOLUME)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame.display.update()


def choose_level():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    bg_image = pygame.image.load('Resources/tiles/Tiles_from_internet/choose level.png')
    screen.blit(bg_image, (0, 0))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # первый уровень, индекс 0
                if 114 <= mouse[0] <= 267 and 456 <= mouse[1] <= 753:
                    game_start(0)
                # второй уровень, индекс 1
                elif 978 <= mouse[0] <= 1134 and 456 <= mouse[1] <= 753:
                    game_start(1)
                # третий уровень, индекс 2
                elif 1554 <= mouse[0] <= 1713 and 456 <= mouse[1] <= 753:
                    game_start(2)

        pygame.display.update()


def start():
    pygame.init()
    ctypes.windll.user32.SetProcessDPIAware()
    screen = pygame.display.set_mode((640, 480))
    main_menu(screen)


Music_player = SoundPlayer()
Music_player.play_music(r'resources\music\soundtrack.mp3', SOUND_VOLUME)

start()
