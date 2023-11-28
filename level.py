import pygame
from csv_work import import_csv_layout, import_cut_graphic
from enemy import Enemy
from player import Player
from tile import Tile, StaticTile, Door, AnimatedTile


class Level:
    def __init__(self, level_data, serface):
        self.display_serface = serface

        # переменные для работы с ключами на уровне
        self.keys_get = False

        # СЛОЙ 1 настройка края игрового поля (кирипичей)
        bricks_layout = import_csv_layout(level_data['bricks']) # получаем матрицу с индексами плиток
        self.tile_list = import_cut_graphic('Resources/Tiles/Tiles_from_internet/14-TileSets/Terrain.png', 32, 32) # вырезаем все плитки из общего изображения
        self.bricks_sprites = self.creat_tile_group(bricks_layout, 'bricks') # создаем матрицу с плитками (изображениями) кирпичей

        # СЛОЙ 2 настройка задней стены
        wall_layout = import_csv_layout(level_data['wall']) # получаем матрицу с индексами плиток
        self.wall_sprites = self.creat_tile_group(wall_layout, 'wall') # создаем матрицу с плитками (изображениями) стены

        # СЛОЙ 3 настройка двери
        door_layout = import_csv_layout(level_data['door']) # получаем матрицу с индексами плиток
        self.door_sprites = self.creat_tile_group(door_layout, 'door') # создаем матрицу с плитками (изображениями) двери

        # СЛОЙ 4 настройка ключа
        key_layout = import_csv_layout(level_data['key']) # получаем матрицу с индексами плиток
        self.key_sprites = self.creat_tile_group(key_layout, 'key') # создаем матрицу с плитками (изображениями) ключей

        # СЛОЙ 6 настройка врага
        enemy_layout = import_csv_layout(level_data['enemy']) # получаем матрицу с индексами плиток
        self.enemy_sprites = self.creat_tile_group(enemy_layout, 'enemy') # создаем матрицу с плитками (изображениями) врагов
        self.enemy_stop_sprites = self.creat_tile_group(enemy_layout, 'enemy_stop') # создаем матрицу с плитками-ограничителями движения

        # настройка игрока
        start_stop_layout = import_csv_layout(level_data['start_stop']) # получаем матрицу с индексами плиток
        self.player = self.creat_tile_group(start_stop_layout, 'start') # создаем матрицу с местом старта игрока
        self.end_sprites = self.creat_tile_group(start_stop_layout, 'stop') # создаем матрицу с плитками, завершающими уровень (если координаты игрока совпадают с координатами этих плиток, то уровень считается пройденным)

    def creat_tile_group(self, layout, type):
        # нруппировка игрока отличается от других
        if type == 'start':
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

                    if type == 'bricks' or type == 'wall':
                        # получаем плитку по индексу из списка
                        tile_surface = self.tile_list[int(col)]
                        # создаем статичный объект
                        sprites_group.add(StaticTile(32, 32, x, y, tile_surface))

                    elif type == 'door':
                        # создаем объект класса дверь (изображение будет полгружаться внутри)
                        sprites_group.add(Door(46, 56, x, y))

                    elif type == 'key':
                        # создаем анимированный объект
                        sprites_group.add(AnimatedTile(32, 32, x, y, 'Resources/Tiles/Tiles_from_internet/15-Key'))

                    elif type == 'enemy' and col == '0': # сам враг
                        # создаем объект класса враг
                        sprites_group.add(Enemy(x, y))

                    elif type == 'enemy_stop' and col == '1': # ограничители для врагов
                        # создаем объект, нам не так важен класс, главное - его расположение
                        sprites_group.add(Tile(32, 32, x, y))

                    elif type == 'start' and col == '0':
                        # создаем объект игрока
                        sprites_group.add(Player((x, y)))


                    elif type == 'stop' and col == '1': # конец уровня
                        # создаем объект, нам не так важен класс, главное - его расположение
                        sprites_group.add(Tile(32, 32, x, y))

        return sprites_group

    # разворот врага при встрече ограничителя
    def enemy_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.enemy_stop_sprites, False):
                enemy.reverse()

    # взятие ключа
    def key_getting(self):
        # роверяем, что на уровне еще есть ключи
        if not self.keys_get:
            player = self.player.sprite

            for key in self.key_sprites.sprites():
                if key.rect.colliderect(player.rect): # если расположения совпадают
                    key.kill()  # удаляем получееный ключ из всех групп
                    if len(self.key_sprites) == 0:
                        self.keys_get = True # если собрали все ключи

                        for door in self.door_sprites.sprites():
                            # вызываем метод, который открывает дверь, если собраны все ключи
                            door.animate()

    # не даем выйти игроку за рамки уровня по горизонтали
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed # меняем расположение игрока

        for sprite in self.bricks_sprites.sprites():
            if sprite.rect.colliderect(player.rect): # если координаты гг и кирпичей совпадают, то

                if player.direction.x < 0: # если двигался налево, двигаем направо
                    player.rect.left = sprite.rect.right

                elif player.direction.x > 0: # если двигался направо, двигаем налево
                    player.rect.right = sprite.rect.left

    # не даем выйти игроку за рамки уровня по вертикали
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity() # 'включаем' гравитацию

        for sprite in self.bricks_sprites.sprites():
            if sprite.rect.colliderect(player.rect):# если координаты гг и кирпичей совпадают, то

                if player.direction.y > 0: # если двигался вниз, двигаем вверх
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0 # обнуляем направление, чтобы не накапливалась гравитация
                    player.on_ground = True # переменная для прыжка (прыгаем только с кирпичей)

                elif player.direction.y < 0: # если двигался вверх, двигаем вниз
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ground = False

    # проверяем пройден ли уровень
    def the_end_of_level(self):
        player = self.player.sprite

        for sprite in self.end_sprites.sprites():
            # если координаты гг и координаты плиток финища совпадают и все ключи собраны, пока меняеем цвет
            if sprite.rect.colliderect(player.rect) and len(self.key_sprites) == 0:
                player.image.fill('black')

    def run(self):
        # матрицы с изображением плиток выводятся на экран

        # кирпичи
        self.bricks_sprites.draw(self.display_serface)
        self.bricks_sprites.update()

        # стена
        self.wall_sprites.draw(self.display_serface)
        self.wall_sprites.update()

        # дверь
        self.door_sprites.draw(self.display_serface)
        self.door_sprites.update()

        # ключ
        self.key_sprites.draw(self.display_serface)
        self.key_getting() # проверяем, не взяли ли ключ
        self.key_sprites.update()

        # враги
        self.enemy_sprites.draw(self.display_serface)
        self.enemy_sprites.update()
        self.enemy_reverse() # не надо ли развернуться

        # игрок
        self.player.update()
        self.horizontal_movement_collision() # достигли ли кирпичей по горизонтали
        self.vertical_movement_collision() # достигли ли кирпичей по вертикали
        self.the_end_of_level() # дошли ли до конца
        self.player.draw(self.display_serface)

