import pygame
from csv_work import import_folder, import_cut_graphic


class Tile(pygame.sprite.Sprite):
    def __init__(self, size_x, size_y, x, y):
        super().__init__()

        self.image = pygame.Surface((size_x, size_y))
        self.rect = self.image.get_rect(topleft=(x, y))


class StaticTile(Tile):
    def __init__(self, size_x, size_y, x, y, surface):
        super().__init__(size_x, size_y, x, y)
        self.image = surface


class Door(Tile):
    def __init__(self, size_x, size_y, x, y):
        super().__init__(size_x, size_y, x, y)
        #  переменная, чтобы не начать анимацию раньше времени
        self.go_animated = False

        # вырезаем все плитки, подготавливаем первую картинку двери
        self.frame_index = 0
        self.frames = import_cut_graphic('Resources/Tiles/Tiles_from_internet/11-Door/door1.png', 64, 64)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(bottomleft=(x, y))

    def animate(self):
        # первоначально вызываем из level, если все ключи собраны, далее вызывем в функции updete
        self.go_animated = True
        self.frame_index += 0.12

        # так как анимацию нужно показать только один раз, делаем проверку индекса
        if self.frame_index <= 5:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        if self.go_animated:
            self.animate()


class AnimatedTile(Tile):
    def __init__(self, size_x, size_y, x, y, way):
        super().__init__(size_x, size_y, x, y)
        self.frames = import_folder(way)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self, speed):
        self.frame_index += speed
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, speed=0.15):
        self.animate(speed)
