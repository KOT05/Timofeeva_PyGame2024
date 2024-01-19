import ctypes
import sys
import os
from level import Level
from level_data import all_levels
from functions import *

WIDTH, HEIGHT = 1920, 1080
SOUND_VOLUME = 0.05
max_ind = {'0'}
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
                if level_ind == 5:
                    final_window()
                else:
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
def main_menu(show_results=False, replay_music=False):
    screen = pygame.display.set_mode((757, 950))
    bg_image = pygame.image.load('Resources/tiles/Tiles_from_internet/Заставка 3-4.jpg')
    screen.blit(bg_image, (0, 0))

    if show_results:  # при наличии аргумента результаты отобразятся на финальном окне
        final_window()

    if replay_music:
        # первый санудтрек
        Music_player.play_music(r'Resources\music\soundtrack.mp3', SOUND_VOLUME)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # играть
                if 246 <= mouse[0] <= 486 and 358 <= mouse[1] <= 422:
                    Music_player.play_music(r'resources\music\soundtrack_2.mp3', SOUND_VOLUME)
                    stopwatch.start()
                    choose_level(screen)
                    break
                # обучение
                elif 204 <= mouse[0] <= 531 and 451 <= mouse[1] <= 525:
                    learning()
                    break
                # настройки
                elif 190 <= mouse[0] <= 557 and 557 <= mouse[1] <= 626:
                    settings_menu(screen)
                    break
                # выход
                elif 261 <= mouse[0] <= 484 and 659 <= mouse[1] <= 735:
                    sys.exit()

        pygame.display.update()


# меню настроек
def settings_menu(screen):
    bg_image = pygame.image.load('Resources/tiles/Tiles_from_internet/Настройки.jpg')
    screen.blit(bg_image, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # звук
                if 242 <= mouse[0] <= 497 and 387 <= mouse[1] <= 481:
                    audio_settings(screen)
                    break
                # видео
                elif 232 <= mouse[0] <= 517 and 503 <= mouse[1] <= 608:
                    video_settings(screen)
                    break
                # назад
                elif 237 <= mouse[0] <= 645 and 504 <= mouse[1] <= 729:
                    main_menu(show_results=False, replay_music=True)
                    break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu(show_results=False, replay_music=True)
                break

        pygame.display.update()


# настройки видео
def video_settings(screen):
    global WIDTH, HEIGHT
    bg_image = pygame.image.load('Resources/tiles/Tiles_from_internet/Настройки видео.jpg')
    screen.blit(bg_image, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # 800x600
                if 186 <= mouse[0] <= 544 and 384 <= mouse[1] <= 474:
                    WIDTH, HEIGHT = 800, 600
                    settings_menu(screen)
                    break
                # 1280x720
                elif 164 <= mouse[0] <= 524 and 530 <= mouse[1] <= 615:
                    WIDTH, HEIGHT = 1280, 720
                    settings_menu(screen)
                    break
                # 1920x1080
                elif 147 <= mouse[0] <= 664 and 593 <= mouse[1] <= 754:
                    WIDTH, HEIGHT = 1920, 1080
                    settings_menu(screen)
                    break
                # выход
                elif 242 <= mouse[0] <= 791 and 508 <= mouse[1] <= 881:
                    settings_menu(screen)
                    break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                settings_menu(screen)
                break

        pygame.display.update()


# настройки аудио
def audio_settings(screen):
    global SOUND_VOLUME
    bg_image = pygame.image.load('Resources/tiles/Tiles_from_internet/Настройки звука.png')
    screen.blit(bg_image, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # выход
                if 240 <= mouse[0] <= 515 and 842 <= mouse[1] <= 933:
                    break
                # 100 %
                elif 261 <= mouse[0] <= 481 and 315 <= mouse[1] <= 406:
                    SOUND_VOLUME = 0.1
                    settings_menu(screen)
                # 50 %
                elif 278 <= mouse[0] <= 461 and 442 <= mouse[1] <= 522:
                    SOUND_VOLUME = 0.05
                    settings_menu(screen)
                # 25 %
                elif 286 <= mouse[0] <= 456 and 276 <= mouse[1] <= 660:
                    SOUND_VOLUME = 0.025
                    settings_menu(screen)
                # ON/OFF
                elif 186 <= mouse[0] <= 586 and 697 <= mouse[1] <= 801:
                    if SOUND_VOLUME == 0:
                        SOUND_VOLUME = 0.1
                    else:
                        SOUND_VOLUME = 0
                    settings_menu(screen)
                Music_player.set_volume(SOUND_VOLUME)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                settings_menu(screen)
                break

        pygame.display.update()


# меню выбора уровня
def choose_level(screen):
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    bg_image = pygame.image.load(
        f'Resources/tiles/Tiles_from_internet/25-Choose level/choose level{len(max_ind)}.png')
    screen.blit(bg_image, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu(show_results=True, replay_music=True)
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
                elif 1548 <= mouse[0] <= 1710 and 543 <= mouse[1] <= 847 and len(max_ind) > 5:
                    game_start(5)
                # кнопка назад
                elif 1730 <= mouse[0] <= 1891 and 21 <= mouse[1] <= 74:
                    main_menu(show_results=True, replay_music=True)

        pygame.display.update()


# окно подсчёта результатов
def final_window():
    screen = pygame.display.set_mode((757, 950))
    stopwatch.stop()
    result_time = round(stopwatch.elapsed_time())
    stopwatch.reset()
    hours, minutes, seconds = transform_time(result_time)

    bg_image = pygame.image.load('Resources/tiles/Tiles_from_internet/Финал.png')
    screen.blit(bg_image, (0, 0))

    render_of_text(screen, f'{len(max_ind)}', (590, 504), size=95)
    render_of_text(screen,
                   f'{hours} часов {minutes} минут {seconds} секунд',
                   (370, 705), size=64)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                main_menu(show_results=False, replay_music=True)
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main_menu(show_results=False, replay_music=True)
                break

        pygame.display.update()


# заставка
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
                main_menu(show_results=False, replay_music=True)

        pygame.display.update()


# вывод обучения
def learning():
    screen = pygame.display.set_mode((1200, 900))

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
                main_menu(show_results=False, replay_music=True)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main_menu(show_results=False, replay_music=True)

        pygame.display.update()


# функция инициализации программы
def start():
    pygame.init()
    ctypes.windll.user32.SetProcessDPIAware()
    screen = pygame.display.set_mode((757, 950))
    start_window(screen)


# запуск кода
start()
