import pygame
import sys
from level import Level
from level_data import all_levels

# настройки pygame
pygame.init()
screen = pygame.display.set_mode((1600, 832))
clock = pygame.time.Clock()

# выбор уровня
level_ind = 0
level = Level(all_levels[level_ind], screen)


def resturt_button(lv, pos):
    for sprite in lv.button_sprites.sprites():
        if sprite.rect.colliderect(pos[0], pos[1], 1, 1):
            return True



while True:
    # выход
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # заливка фона
    screen.fill((63, 56, 81))

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
        if resturt_button(level, pygame.mouse.get_pos()):
            level = Level(all_levels[level_ind], screen)

    # проверка смерти
    if level.should_restart:
        level = Level(all_levels[level_ind], screen)
        level.should_restart = False

    # запуск уровня
    level.run()

    pygame.display.update()
    clock.tick(60)
