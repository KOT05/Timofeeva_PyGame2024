import ctypes
import sys
import os
from level import Level
from level_data import all_levels
from functions import *

WIDTH, HEIGHT = 1920, 1080
SOUND_VOLUME = 0.05
max_ind = set('0')
Music_player = SoundPlayer()
stopwatch = Stopwatch()


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
def main_menu(screen, show_results=False, replay_music=False):
    pygame.display.set_mode((640, 480))

    if show_results:  # при наличии аргумента результаты отобразятся на финальном окне
        final_window(screen)

    if replay_music:
        # первый санудтрек
        Music_player.play_music(r'Resources\music\soundtrack.mp3', SOUND_VOLUME)

    # объекты-кнопки
    start_button = Button('ИГРАТЬ', (250, 150), 150, 50, 'gray', 'red', 'yellow', 30)
    settings_button = Button('НАСТРОЙКИ', (250, 210), 150, 50, 'black', 'red', 'yellow', 30)
    exit_button = Button('ВЫХОД', (250, 270), 150, 50, 'green', 'red', 'yellow', 30)

    running = True
    while running:
        # отрисовка основных элементов на экране
        rendering(screen, r'Resources\Images\dream_TradingCard(2).jpg', (640, 480))
        # отрисовка заголовка
        render_of_text(screen, 'ПОБЕГ', (320, 100))

        # отрисовка кнопок
        start_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_hovered(event.pos):
                    Music_player.play_music(r'resources\music\soundtrack_2.mp3', SOUND_VOLUME)
                    stopwatch.start()
                    choose_level(screen)
                elif exit_button.is_hovered(event.pos):
                    sys.exit()
                elif settings_button.is_hovered(event.pos):
                    settings_menu(screen)

        pygame.display.update()


# меню настроек
def settings_menu(screen):
    audio_button = Button('ЗВУК', (250, 150), 150, 50, 'gray', 'red', 'yellow', 30)
    video_button = Button('ВИДЕО', (250, 210), 150, 50, 'black', 'red', 'yellow', 30)
    exit_button = Button('НАЗАД', (250, 270), 150, 50, 'green', 'red', 'yellow', 30)

    running = True
    while running:
        rendering(screen, r'Resources\Images\dream_TradingCard(2).jpg', (640, 480))
        render_of_text(screen, 'Настройки', (320, 100))

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


# настройки видео
def video_settings(screen):
    global WIDTH, HEIGHT
    resolution_button_1 = Button('800x600', (250, 150), 150, 50, 'gray', 'red', 'yellow', 30)
    resolution_button_2 = Button('1280x720', (250, 210), 150, 50, 'black', 'red', 'yellow', 30)
    resolution_button_3 = Button('1920x1080', (250, 270), 150, 50, 'brown', 'red', 'yellow', 30)
    exit_button = Button('НАЗАД', (250, 330), 150, 50, 'green', 'red', 'yellow', 30)

    running = True
    while running:
        rendering(screen, r'Resources\Images\dream_TradingCard(2).jpg', (640, 480))
        render_of_text(screen, 'ВИДЕО', (320, 100))

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


# настройки аудио
def audio_settings(screen):
    global SOUND_VOLUME
    volume_1 = Button('100%', (250, 150), 150, 50, 'gray', 'red', 'yellow', 30)
    volume_2 = Button('50%', (250, 210), 150, 50, 'black', 'red', 'yellow', 30)
    volume_3 = Button('25%', (250, 270), 150, 50, 'brown', 'red', 'yellow', 30)
    volume_4 = Button('ON/OFF', (250, 330), 150, 50, 'pink', 'red', 'yellow', 30)
    exit_button = Button('НАЗАД', (250, 390), 150, 50, 'green', 'red', 'yellow', 30)

    running = True
    while running:
        rendering(screen, r'Resources\Images\dream_TradingCard(2).jpg', (640, 480))
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
                        SOUND_VOLUME = 0.1
                    elif volume_2.is_hovered(event.pos):
                        SOUND_VOLUME = 0.05
                    elif volume_3.is_hovered(event.pos):
                        SOUND_VOLUME = 0.025
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
                main_menu(screen, show_results=True, replay_music=True)
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
                    main_menu(screen, show_results=True, replay_music=True)

        pygame.display.update()


# окно подсчёта результатов
def final_window(screen):
    stopwatch.stop()
    result_time = round(stopwatch.elapsed_time())
    stopwatch.reset()
    hours, minutes, seconds = result_time // 60 // 60, result_time // 60, result_time

    rendering(screen, r'Resources\Images\dream_TradingCard(2).jpg', (640, 480))
    render_of_text(screen, 'ИТОГО', (320, 50))

    render_of_text(screen, f'УРОВНЕЙ ПРОЙДЕНО:', (160, 150), size=35)
    render_of_text(screen, f'{max(max_ind)}', (30, 200), size=35, color='yellow')
    render_of_text(screen, f'ВРЕМЕНИ В ИГРЕ ПРОВЕДЕНО:', (215, 250), size=35)
    render_of_text(screen,
                   f'{hours} часов {minutes} минут {seconds} секунд',
                   (175, 300), size=35, color='yellow')
    render_of_text(screen, f'Кликни, чтобы вернуться в меню', (320, 450), size=25)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.update()


def start_window(screen):
    # первый санудтрек
    Music_player.play_music(r'Resources\music\soundtrack.mp3', SOUND_VOLUME)

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
                main_menu(screen, show_results=False, replay_music=False)

        pygame.display.update()


# функция инициализации программы
def start():
    pygame.init()
    ctypes.windll.user32.SetProcessDPIAware()
    screen = pygame.display.set_mode((757, 950))
    start_window(screen)


# запуск кода
start()
