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

while True:
    # выход
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # заливка фона
    screen.fill((63, 56, 81))

    if level.should_change:
        level_ind += 1
        print(level_ind)
        level = Level(all_levels[level_ind], screen)
        level.should_change = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        level = Level(all_levels[level_ind], screen)

    # запуск уровня
    level.run()

    pygame.display.update()
    clock.tick(60)
