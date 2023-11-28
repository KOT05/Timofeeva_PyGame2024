import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # создание самого перса (пока квадратик)
        self.image = pygame.Surface((32, 32))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)

        # множество кнопок, которые игнорируются до определенного момента
        self.ignore = set()

        # настройки для движения
        self.on_ground = True
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.gravity = 0.8
        self.jump_speed = -16

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
            self.ignore.add('K_UP') # пока кнопку не отожмут, мы ее игнорим

        elif not keys[pygame.K_UP]: # кнопка отжата, далее не игноририм ее
            self.ignore.discard('K_UP')

    # добавляем гравитацию, чтобы падать после прыжка
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    # прыгаем
    def jump(self):
        if self.on_ground: # прыгать можем только с кирпичей
            self.direction.y = self.jump_speed
            self.on_ground = False

    def update(self):
        self.get_input()

