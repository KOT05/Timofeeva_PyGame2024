import pygame
from csv_work import import_csv_layout, import_cut_graphic
from enemy import Enemy
from player import Player
from tile import Tile, StaticTile, Door, AnimatedTile


class Level:
    def __init__(self, level_data, serface):
        self.display_serface = serface

        self.should_change = False
        self.should_restart = False
        self.ignore_r = False

        # переменные для работы с ключами на уровне
        self.keys_get = False

        # СЛОЙ 1 настройка края игрового поля (кирипичей)
        bricks_layout = import_csv_layout(level_data['bricks'])  # получаем матрицу с индексами плиток
        self.tile_list = import_cut_graphic('Resources/Tiles/Tiles_from_internet/14-TileSets/Terrain.png', 32,
                                            32)  # вырезаем все плитки из общего изображения
        self.bricks_sprites = self.creat_tile_group(bricks_layout, 'bricks')

        # СЛОЙ 2 настройка задней стены
        wall_layout = import_csv_layout(level_data['wall'])  # получаем матрицу с индексами плиток
        self.wall_sprites = self.creat_tile_group(wall_layout, 'wall')

        # СЛОЙ 3 настройка двери
        door_layout = import_csv_layout(level_data['door'])  # получаем матрицу с индексами плиток
        self.door_sprites = self.creat_tile_group(door_layout, 'door')

        # СЛОЙ 4 настройка ключа
        key_layout = import_csv_layout(level_data['key'])  # получаем матрицу с индексами плиток
        self.key_sprites = self.creat_tile_group(key_layout, 'key')

        # СЛОЙ 5 настройка шипов
        thorn_layout = import_csv_layout(level_data['thorn'])  # получаем матрицу с индексами плиток
        self.thorn_sprites = self.creat_tile_group(thorn_layout, 'thorn')

        # СЛОЙ 6 настройка врага
        enemy_layout = import_csv_layout(level_data['enemy'])  # получаем матрицу с индексами плиток
        self.enemy_sprites = self.creat_tile_group(enemy_layout, 'enemy')
        self.enemy_stop_sprites = self.creat_tile_group(enemy_layout, 'enemy_stop')

        # СЛОЙ 7 настройка края игрового поля (кирипичей)
        button_layout = import_csv_layout(level_data['button'])
        self.tile_list = import_cut_graphic('Resources/Tiles/Tiles_from_internet/21-Button/restart.png', 32,
                                            32)  # вырезаем все плитки из общего изображения
        self.button_sprites = self.creat_tile_group(button_layout, 'button')

        # настройка игрока
        start_stop_layout = import_csv_layout(level_data['start_stop'])
        self.player = self.creat_tile_group(start_stop_layout, 'start')
        self.end_sprites = self.creat_tile_group(start_stop_layout, 'stop')

    def creat_tile_group(self, layout, typee):
        # нруппировка игрока отличается от других
        if typee == 'start':
            sprites_group = pygame.sprite.GroupSingle()
        else:
            sprites_group = pygame.sprite.Group()

        # проходимся по матрице слоя с индексами плиток, расчитываем координаты верхнего левого угла
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                # проверяем, что у нас не пустота (пустые плитки идут с индеком -1)
                if col != '-1':
                    x = 32 * col_index
                    y = 32 * row_index

                    if typee == 'bricks' or typee == 'wall':
                        # получаем плитку по индексу из списка
                        tile_surface = self.tile_list[int(col)]
                        # создаем статичный объект
                        sprite = StaticTile(32, 32, x, y, tile_surface)
                        sprites_group.add(sprite)

                    elif typee == 'door':
                        # создаем объект класса дверь (изображение будет полгружаться внутри)
                        sprite = Door(46, 56, x, y)
                        sprites_group.add(sprite)

                    elif typee == 'key':
                        # создаем анимированный объект
                        sprite = AnimatedTile(32, 32, x, y, 'Resources/Tiles/Tiles_from_internet/15-Key')
                        sprites_group.add(sprite)

                    elif typee == 'enemy' and col == '0':  # сам враг
                        # создаем объект класса враг
                        sprite = Enemy(x, y)
                        sprites_group.add(sprite)

                    elif typee == 'enemy_stop' and col == '1':  # ограничители для врагов
                        # создаем объект, нам не так важен класс, главное - его расположение
                        sprite = Tile(32, 32, x, y)
                        sprites_group.add(sprite)

                    elif typee == 'start' and col == '0':
                        sprite = Player((x, y))  # создаем объект игрока
                        sprites_group.add(sprite)

                    elif typee == 'stop' and col == '1':  # конец уровня
                        # создаем объект, нам не так важен класс, главное - его расположение
                        sprite = Tile(32, 32, x, y)
                        sprites_group.add(sprite)

                    elif typee == 'thorn':
                        # создаем статичный объект
                        tile_surface = pygame.image.load(
                            'Resources/Tiles/Tiles_from_internet/20-Thorn/thorn.png').convert_alpha()
                        sprite = StaticTile(32, 32, x, y, tile_surface)
                        sprites_group.add(sprite)

                    elif typee == 'button':
                        # создаем статичный объект
                        tile_surface = self.tile_list[int(col)]
                        sprite = StaticTile(32, 32, x, y, tile_surface)
                        sprites_group.add(sprite)

        return sprites_group

    # разворот врага при встрече ограничителя
    def enemy_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.enemy_stop_sprites, False):
                enemy.reverse()

    # взятие ключа
    def key_getting(self):
        if not self.keys_get:
            player = self.player.sprite

            for key in self.key_sprites.sprites():
                if key.rect.colliderect(player.rect):  # если расположения совпадают
                    key.kill()

                    if len(self.key_sprites) == 0:
                        self.keys_get = True
                        for door in self.door_sprites.sprites():
                            door.animate()

    # падение на шипы
    def thorn_file(self):
        player = self.player.sprite

        for thorn in self.thorn_sprites.sprites():
            if thorn.rect.colliderect(player.rect):  # если расположения совпадают
                self.should_restart = True

    # не даем выйти игроку за рамки уровня по горизонтали
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed  # меняем расположение игрока

        for sprite in self.bricks_sprites.sprites():
            if sprite.rect.colliderect(player.rect):  # если координаты гг и кирпичей совпадают, то

                if player.direction.x < 0:  # если двигался налево, двигаем направо
                    player.rect.left = sprite.rect.right

                elif player.direction.x > 0:  # если двигался направо, двигаем налево
                    player.rect.right = sprite.rect.left

    # не даем выйти игроку за рамки уровня по вертикали
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()  # 'включаем' гравитацию

        for sprite in self.bricks_sprites.sprites():
            if sprite.rect.colliderect(player.rect):  # если координаты гг и кирпичей совпадают, то

                if player.direction.y > 0:  # если двигался вниз, двигаем вверх
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0  # обнуляем направление, чтобы не накапливалась гравитация
                    player.on_ground = True  # переменная для прыжка (прыгаем только с кирпичей)

                elif player.direction.y < 0:  # если двигался вверх, двигаем вниз
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ground = False

    # проверяем пройден ли уровень
    def the_end_of_level(self):
        player = self.player.sprite

        for sprite in self.end_sprites.sprites():
            # если координаты гг и координаты плиток финиша совпадают и все ключи собраны, пока меняеем цвет
            if sprite.rect.colliderect(player.rect) and self.keys_get:
                self.should_change = True

    def portal(self):
        player = self.player.sprite
        return player.portal_sprites

    def run(self):
        # матрицы с изображением плиток выводятся на экран

        # кирпичи
        self.bricks_sprites.draw(self.display_serface)

        # стена
        self.wall_sprites.draw(self.display_serface)

        # дверь
        self.door_sprites.draw(self.display_serface)
        self.door_sprites.update()

        # ключ
        self.key_sprites.draw(self.display_serface)
        self.key_getting()  # проверяем, не взяли ли ключ
        self.key_sprites.update()

        # шипы
        self.thorn_sprites.draw(self.display_serface)
        self.thorn_file()

        # портал
        portal = self.portal()
        portal.draw(self.display_serface)
        portal.update()

        # враги
        self.enemy_sprites.draw(self.display_serface)
        self.enemy_sprites.update()
        self.enemy_reverse()  # не надо ли развернуться

        # кнопка restart
        self.button_sprites.draw(self.display_serface)

        # игрок
        self.player.update()
        self.horizontal_movement_collision()  # достигли ли кирпичей по горизонтали
        self.vertical_movement_collision()  # достигли ли кирпичей по вертикали
        self.the_end_of_level()  # дошли ли до конца
        self.player.draw(self.display_serface)