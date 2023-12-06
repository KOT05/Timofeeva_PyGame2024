import pygame
from tile import AnimatedTile
from csv_work import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # создание самого перса (пока квадратик)
        self.frames = import_folder('Resources/Tiles/Tiles_from_internet/18-Main character/Idle Blink')
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect(bottomleft=pos)

        # множество кнопок, которые игнорируются до определенного момента
        self.ignore = set()

        # настройки для движения
        self.on_ground = True
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.gravity = 0.8
        self.jump_speed = -16

        # настройки для портала
        self.space_kol = 0
        self.portal_sprites = pygame.sprite.Group()

    # управление персом
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]: # стрелка вправо нажата
            self.direction.x = 1
        elif keys[pygame.K_LEFT]: # стрелка влево нажата
            self.direction.x = -1
        else:
            self.direction.x = 0

        # если стрелка вверх нажата, и ее нет в игнориремых, то прыгаем
        if keys[pygame.K_UP] and 'K_UP' not in self.ignore:
            self.jump()
            self.ignore.add('K_UP')  # пока кнопку не отожмут, мы ее игнорим

        elif not keys[pygame.K_UP]: # кнопка отжата, далее не игноририм ее
            self.ignore.discard('K_UP')

        # если space, и ее нет в игнориремых, то вызываем функциюю portal()
        if keys[pygame.K_SPACE] and 'K_SPACE' not in self.ignore:
            self.space_kol += 1
            self.portal()
            self.ignore.add('K_SPACE')  # пока кнопку не отожмут, мы ее игнорим

        elif not keys[pygame.K_SPACE]:  # кнопка отжата, далее не игноририм ее
            self.ignore.discard('K_SPACE')


    # добавляем гравитацию, чтобы падать после прыжка
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    # прыгаем
    def jump(self):
        if self.on_ground: # прыгать можем только с кирпичей
            self.direction.y = self.jump_speed
            self.on_ground = False

    def animate(self):
        self.frame_index += 0.15
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self):
        self.get_input()
        self.animate()

    # работа с порталом
    def portal(self):
        # если нечетное количество нажатий кнопки, то создаем портал
        if self.space_kol % 2 == 1:
            # получаем координаты для портала
            self.portal_x = self.rect.x
            self.portal_y = self.rect.y + 8

            # добавляем в группу портал, чтобы он отрисовывался
            self.portal_sprites.add(AnimatedTile(32, 32, self.portal_x, self.portal_y, 'Resources/Tiles/Tiles_from_internet/19-Portal'))

        # если четное, то перемещаем игрока на место портала
        elif self.space_kol != 0:
            # перемещаем игрока на координаты портала и игнорируем прыжок
            self.rect.x = self.portal_x
            self.rect.y = self.portal_y
            self.on_ground = False

            # заново создаем пустую группу, чтобы портал не рисовался
            self.portal_sprites = pygame.sprite.Group()
