import pygame
import ctypes
import sys
from level import Level
from level_data import all_levels
from functions import Button, rendering

WIDTH, HEIGHT = 1920, 1080


def restart_button(lv, pos):
    for sprite in lv.button_sprites.sprites():
        if sprite.rect.colliderect(pos[0], pos[1], 1, 1):
            return True


def game_start():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    # выбор уровня
    level_ind = 0
    level = Level(all_levels[level_ind], screen)

    running = True
    while running:
        # выход
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # заливка фона
        screen.fill((2, 1, 32))

        # переход к другому уровню
        if level.should_change:
            level_ind += 1
            level = Level(all_levels[level_ind], screen)
            level.should_change = False

        # проверка кнопки R на клавиатуре
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            level = Level(all_levels[level_ind], screen)

        # выход через esc
        if keys[pygame.K_ESCAPE]:
            running = False
            main_menu(main_screen)

        # проверка кнопки restart на экране
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            if restart_button(level, pygame.mouse.get_pos()):
                level = Level(all_levels[level_ind], screen)

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
        rendering(screen, 'Побег', 'Resources\Images\dream_TradingCard.jpg', (640, 480), (320, 100))

        start_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_hovered(event.pos):
                    game_start()
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
        rendering(screen, 'Настройки', 'Resources\Images\dream_TradingCard.jpg', (640, 480), (320, 100))

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
                    video_settings(main_screen)
                elif exit_button.is_hovered(event.pos):
                    running = False
            if event.type == pygame.K_ESCAPE:
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
        rendering(screen, 'Разрешение экрана', 'Resources\Images\dream_TradingCard.jpg', (640, 480), (320, 100))

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

        pygame.display.update()


def audio_settings(screen):
    exit_button = Button('Выход', (250, 330), 150, 50, 'green', 'red', 'purple', 40)

    running = True
    while running:
        rendering(screen, 'Настройки звука', 'Resources\Images\dream_TradingCard.jpg', (640, 480), (320, 100))

        exit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.is_hovered(event.pos):
                    running = False

        pygame.display.update()


pygame.init()
ctypes.windll.user32.SetProcessDPIAware()
main_screen = pygame.display.set_mode((640, 480))
main_menu(main_screen)
