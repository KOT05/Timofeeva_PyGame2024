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

        self.go_animated = False
        self.frame_index = 0
        self.frames = import_cut_graphic('Resources/Tiles/Tiles_from_internet/11-Door/Opening (46x56).png', 46, 56)

        self.image = pygame.image.load('Resources/Tiles/Tiles_from_internet/11-Door/Idle.png').convert_alpha()
        offset_y = y + 32
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))

    def update(self, changes=False):
        if changes:
            self.go_animated = True

        if self.go_animated:
            self.animate()

    def animate(self):
        self.frame_index += 0.1
        ind = int(self.frame_index % len(self.frames))
        self.image = self.frames[ind]

        if ind == 4 and self.frame_index > 1:
            self.go_animated = False


class AnimatedTile(Tile):
    def __init__(self, size_x, size_y, x, y, way):
        super().__init__(size_x, size_y, x, y)
        self.frames = import_folder(way)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self):
        self.animate()

    def getting_key(self, keys_on_get, door):
        self.frames = [pygame.image.load('Resources/Tiles/Tiles_from_internet/Пустое.png').convert_alpha()]
        if keys_on_get:
            door.update(True)
            # дверь должна начать анимироваться
