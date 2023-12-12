import pygame
import ctypes
import sys
from level import Level
from level_data import all_levels
from classes import Button


def restart_button(lv, pos):
    for sprite in lv.button_sprites.sprites():
        if sprite.rect.colliderect(pos[0], pos[1], 1, 1):
            return True


def game_start():
    screen = pygame.display.set_mode((1600, 832))
    clock = pygame.time.Clock()

    # выбор уровня
    level_ind = 0
    level = Level(all_levels[level_ind], screen)

    while True:
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
    start_button = Button('Играть', (250, 150), 150, 50, 'green', 'red', 'purple', 40)
    settings_button = Button('Настройки', (250, 210), 150, 50, 'green', 'red', 'purple', 40)
    exit_button = Button('Выход', (250, 270), 150, 50, 'green', 'red', 'purple', 40)

    running = True
    while running:
        screen.fill((0, 0, 0))
        main_background = pygame.image.load('Resources\Images\dream_TradingCard.jpg')
        main_background = pygame.transform.scale(main_background, (640, 480))
        screen.blit(main_background, (0, 0))
        start_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)

        font = pygame.font.Font(None, 80)
        text_surface = font.render("Побег", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(320, 100))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_hovered(event.pos):
                    game_start()
                elif exit_button.is_hovered(event.pos):
                    running = False
                elif settings_button.is_hovered(event.pos):
                    pass
        pygame.display.flip()


pygame.init()
ctypes.windll.user32.SetProcessDPIAware()
size = width, height = 640, 480
screen = pygame.display.set_mode(size)
main_menu(screen)
