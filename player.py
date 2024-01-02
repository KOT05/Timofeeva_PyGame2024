import pygame
from tile import AnimatedTile
from csv_work import import_cut_graphic


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.import_charecter_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # множество кнопок, которые игнорируются до определенного момента
        self.ignore = set()

        # настройки для движения
        self.on_ground = True
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4.5
        self.gravity = 0.9
        self.jump_speed = -18

        # настройки для портала
        self.space_kol = 0
        self.portal_sprites = pygame.sprite.Group()

        # настройки для анимации
        self.status = 'idle'
        self.facing_right = True

    # управление персом
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # стрелка вправо нажата
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:  # стрелка влево нажата
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        # если стрелка вверх нажата, и ее нет в игнориремых, то прыгаем
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and 'K_UP' not in self.ignore:
            self.frame_index = 0
            self.jump()
            self.ignore.add('K_UP')  # пока кнопку не отожмут, мы ее игнорим

        elif not (keys[pygame.K_UP] or keys[pygame.K_w]):  # кнопка отжата, далее не игноририм ее
            self.ignore.discard('K_UP')

        # если space, и ее нет в игнориремых, то вызываем функциюю portal()
        if keys[pygame.K_SPACE] and 'K_SPACE' not in self.ignore:
            self.space_kol += 1
            self.portal()
            self.ignore.add('K_SPACE')  # пока кнопку не отожмут, мы ее игнорим

        elif not keys[pygame.K_SPACE]:  # кнопка отжата, далее не игноририм ее
            self.ignore.discard('K_SPACE')

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 0:
            self.status = 'fall'
        elif self.direction.x != 0:
            self.status = 'run'
        else:
            self.status = 'idle'

    # добавляем гравитацию, чтобы падать после прыжка
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    # прыгаем
    def jump(self):
        if self.on_ground:  # прыгать можем только с кирпичей
            self.direction.y = self.jump_speed
            self.on_ground = False

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()

    # работа с порталом
    def portal(self):
        # если нечетное количество нажатий кнопки, то создаем портал
        if self.space_kol % 2 == 1:
            # получаем координаты для портала
            self.portal_x = self.rect.x
            self.portal_y = self.rect.y + 16

            # добавляем в группу портал, чтобы он отрисовывался
            self.portal_sprites.add(
                AnimatedTile(32, 32, self.portal_x, self.portal_y, 'Resources/Tiles/Tiles_from_internet/19-Portal'))

        # если четное, то перемещаем игрока на место портала
        elif self.space_kol != 0:
            # перемещаем игрока на координаты портала и игнорируем прыжок
            self.rect.x = self.portal_x
            self.rect.y = self.portal_y
            self.on_ground = False

            # заново создаем пустую группу, чтобы портал не рисовался
            self.portal_sprites = pygame.sprite.Group()

    def import_charecter_assets(self):
        idle = import_cut_graphic('Resources/Tiles/Tiles_from_internet/18-Main character/idle_new.png', 38, 48)
        run = import_cut_graphic('Resources/Tiles/Tiles_from_internet/18-Main character/run_new.png', 48, 48)
        jump = import_cut_graphic('Resources/Tiles/Tiles_from_internet/18-Main character/jump_new.png', 48, 48)
        fall = import_cut_graphic('Resources/Tiles/Tiles_from_internet/18-Main character/fall_new.png', 48, 48)

        self.animations = {'idle': idle, 'run': run, 'jump': jump, 'fall': fall}
