import pygame
import sys
from level import Level
from level_data import level_0

# настройки pygame
pygame.init()
screen = pygame.display.set_mode((1600, 832))
clock = pygame.time.Clock()

# выбор уровня
level = Level(level_0, screen)

while True:
    # выход
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # заливка фона
    screen.fill((63, 56, 81))

    # запуск уровня
    level.run()

    pygame.display.update()
    clock.tick(60)
