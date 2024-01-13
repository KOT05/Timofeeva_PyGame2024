import pygame
import ctypes
import sys
import os
from level import Level
from level_data import all_levels
from functions import Button, rendering, render_of_text, SoundPlayer

WIDTH, HEIGHT = 1920, 1080
SOUND_VOLUME = 0.25
max_ind = set('0')

# музыка
Music_player = SoundPlayer()

# данные статистики
stat = []


# запуск игры
def game_start(level_ind):
    global max_ind
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    # выбор уровня
    level = Level(all_levels[level_ind], screen)

    running = True
    while running:
        # если пауза
        if level.pause:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    # начать заново
                    if 616 <= mouse[0] <= 750 and 464 <= mouse[1] <= 596:
                        level.pause = False
                        level = Level(all_levels[level_ind], screen)
                    # продолжить
                    elif 884 <= mouse[0] <= 1016 and 464 <= mouse[1] <= 596:
                        level.pause = False
                    # к выбору уровня
                    elif 1168 <= mouse[0] <= 1300 and 464 <= mouse[1] <= 596:
                        level.pause = False
                        choose_level(screen)
                        running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        level.pause = False
                    elif event.key == pygame.K_m:
                        level.pause = False
                        choose_level(screen)
                    elif event.key == pygame.K_r:
                        level.pause = False
                        level = Level(all_levels[level_ind], screen)
        # если паузы нет
        else:
            for event in pygame.event.get():
                # выход
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # если нажали esc, возвращаемся к меню выбора уровня
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    choose_level(screen)
                # если нажали r, то уровень начинается заново
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    level = Level(all_levels[level_ind], screen)
                # если нажали p, то пауза
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    level.pause = True
                # если нажали m, то к окну выбору уровня
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    choose_level(screen)
                # проверка кнопки pause на экране
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for sprite in level.button_sprites.sprites():
                        # если координаты курсора совпадают с кнопкой, то уровень начинается заново
                        if sprite.rect.colliderect(mouse_pos[0], mouse_pos[1], 1, 1):
                            level.pause = True

            screen.fill((6, 5, 13))

            # переход к другому уровню
            if level.should_change:
                level_ind += 1
                max_ind.add(level_ind)
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


# главное меню
def main_menu(*results):
    screen = pygame.display.set_mode((757, 950))
    bg_image = pygame.image.load('Resources/tiles/Tiles_from_internet/Заставка 3-4.jpg')
    screen.blit(bg_image, (0, 0))

    if results:  # при наличии переданных результатов они отобразятся на финальном окне
        final_window(screen)

    # первый санудтрек
    Music_player.play_music(r'resources\music\soundtrack.mp3', SOUND_VOLUME)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # играть
                if 246 <= mouse[0] <= 486 and 358 <= mouse[1] <= 422:
                    Music_player.play_music(r'resources\music\soundtrack_2.mp3', SOUND_VOLUME)
                    running = False
                    choose_level(screen)
                # обучение
                elif 204 <= mouse[0] <= 531 and 451 <= mouse[1] <= 525:
                    running = False
                    learning()
                # настройки
                elif 190 <= mouse[0] <= 557 and 557 <= mouse[1] <= 626:
                    running = False
                    settings_menu(screen)
                # выход
                elif 261 <= mouse[0] <= 484 and 659 <= mouse[1] <= 735:
                    running = False
                    sys.exit()

        pygame.display.update()


# меню настроек
def settings_menu(screen):
    bg_image = pygame.image.load('Resources/tiles/Tiles_from_internet/Настройки.jpg')
    screen.blit(bg_image, (0, 0))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # звук
                if 242 <= mouse[0] <= 497 and 387 <= mouse[1] <= 481:
                    running = False
                    audio_settings(screen)
                # видео
                elif 232 <= mouse[0] <= 517 and 503 <= mouse[1] <= 608:
                    running = False
                    video_settings(screen)
                # назад
                elif 237 <= mouse[0] <= 645 and 504 <= mouse[1] <= 729:
                    running = False
                    main_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                main_menu()

        pygame.display.update()


# настройки видео
def video_settings(screen):
    global WIDTH, HEIGHT
    bg_image = pygame.image.load('Resources/tiles/Tiles_from_internet/Настройки видео.jpg')
    screen.blit(bg_image, (0, 0))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # 800x600
                if 186 <= mouse[0] <= 383 and 550 <= mouse[1] <= 467:
                    running = False
                    WIDTH, HEIGHT = 800, 600
                # 1280x720
                elif 164 <= mouse[0] <= 524 and 570 <= mouse[1] <= 615:
                    running = False
                    WIDTH, HEIGHT = 1280, 720
                # 1920x1080
                elif 147 <= mouse[0] <= 664 and 593 <= mouse[1] <= 754:
                    running = False
                    WIDTH, HEIGHT = 1920, 1080
                # выход
                elif 242 <= mouse[0] <= 791 and 508 <= mouse[1] <= 881:
                    running = False
                    settings_menu(screen)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                settings_menu(screen)

        pygame.display.update()


# настройки аудио
def audio_settings(screen):
    global SOUND_VOLUME
    volume_1 = Button('100%', (250, 150), 150, 50, 'green', 'red', 'purple', 30)
    volume_2 = Button('50%', (250, 210), 150, 50, 'green', 'red', 'purple', 30)
    volume_3 = Button('25%', (250, 270), 150, 50, 'green', 'red', 'purple', 30)
    volume_4 = Button('ON/OFF', (250, 330), 150, 50, 'green', 'red', 'purple', 30)
    exit_button = Button('НАЗАД', (250, 390), 150, 50, 'green', 'red', 'purple', 30)

    running = True
    while running:
        rendering(screen, r'Resources\Images\dream_TradingCard.jpg', (640, 480))
        render_of_text(screen, 'ЗВУК', (320, 100))

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


# меню выбора уровня
def choose_level(screen):
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    bg_image = pygame.image.load(
        f'Resources/tiles/Tiles_from_internet/25-Choose level/choose level{len(max_ind)}.png')
    screen.blit(bg_image, (0, 0))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu(stat)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # первый уровень, индекс 0
                if 114 <= mouse[0] <= 270 and 135 <= mouse[1] <= 432:
                    game_start(0)
                # второй уровень, индекс 1
                elif 633 <= mouse[0] <= 786 and 135 <= mouse[1] <= 432 and len(max_ind) > 1:
                    game_start(1)
                # третий уровень, индекс 2
                elif 1500 <= mouse[0] <= 1656 and 135 <= mouse[1] <= 432 and len(max_ind) > 2:
                    game_start(2)
                # четвертый уровень, индекс 3
                elif 111 <= mouse[0] <= 267 and 546 <= mouse[1] <= 846 and len(max_ind) > 3:
                    game_start(3)
                # пятый уровень, индекс 4
                elif 975 <= mouse[0] <= 1131 and 546 <= mouse[1] <= 846 and len(max_ind) > 4:
                    game_start(4)
                # шестой уровень, индекс 5
                elif 978 <= mouse[0] <= 1134 and 1545 <= mouse[1] <= 1701 and len(max_ind) > 5:
                    game_start(5)
                # кнопка назад
                elif 1730 <= mouse[0] <= 1891 and 21 <= mouse[1] <= 74:
                    main_menu(stat)

        pygame.display.update()


# окно подсчёта результатов
def final_window(screen):
    rendering(screen, r'Resources\Images\dream_TradingCard.jpg', (640, 480))
    render_of_text(screen, 'ИТОГО', (320, 100))

    render_of_text(screen, f'ВРЕМЕНИ В ИГРЕ ПРОВЕДЕНО: ', (205, 150), size=35)
    render_of_text(screen, f'УРОВНЕЙ ПРОЙДЕНО: {max(max_ind)}', (150, 250), size=35)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.update()


def start_window(screen):
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    bg_image = pygame.image.load('Resources/tiles/Tiles_from_internet/Заставка 3 готовая.jpg')
    screen.blit(bg_image, (0, 0))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main_menu()

        pygame.display.update()


# вывод обучения
def learning():
    screen = pygame.display.set_mode((1480, 1020))

    running = True
    ind = 0
    while running:
        screen.fill((6, 5, 13))
        bg_image = pygame.image.load(f'Resources/tiles/Tiles_from_internet/26-Learning/{int(ind % 8) + 1}.png')
        screen.blit(bg_image, (0, 0))
        ind += 0.25

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main_menu()

        pygame.display.update()


# функция инициализации программы
def start():
    pygame.init()
    ctypes.windll.user32.SetProcessDPIAware()
    screen = pygame.display.set_mode((757, 950))
    start_window(screen)


# запуск кода
start()
