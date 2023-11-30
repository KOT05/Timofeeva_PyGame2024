from csv import reader
import pygame
from os import walk


# получаем несколько отдельных изображений, которые образовывают единую анимацию
def import_folder(way):
    surface_list = []

    for _, __, image_files in walk(way):
        for image in image_files:
            full_way = way + '/' + image
            image_surf = pygame.image.load(full_way).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


# чтение csv файла с индексами плиток
def import_csv_layout(way):
    with open(way) as map:
        level = reader(map, delimiter=',')
        scv_map = [list(row) for row in level]

        return scv_map


# из одного изображения с несколькими плитками вырезаем каждую
def import_cut_graphic(way, size_x, size_y):
    # файл с изображением нескольких плиток
    surface = pygame.image.load(way).convert_alpha()

    # количетво плиток по вертикали и геризонтали
    tile_num_x = int(surface.get_size()[0] / size_x)
    tile_num_y = int(surface.get_size()[1] / size_y)

    cut_tiles = []

    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * size_x
            y = row * size_y

            # создаем квадрат для плитки
            new_surf = pygame.Surface((size_x, size_y), flags=pygame.SRCALPHA)
            # вставляем в (0, 0) вырезанный четырехугольник из общего файла
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, size_x, size_y))
            cut_tiles.append(new_surf)

    return cut_tiles
