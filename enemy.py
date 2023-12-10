from csv_work import import_folder
import pygame
from random import randint


class Suriken(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.speed = 3

        # из общего изображения вырезаем плитки для анимации
        self.frames = import_folder('Resources/Tiles/Tiles_from_internet/22-Suriken')
        self.frame_index = 0
        # выбираем первое изображение и загружаем
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        # смещаем вниз, чтобы враг не летал, а касался кирпичей
        # self.rect.y += 8

    def update(self):
        self.animate()

    def animate(self):
        # плавно меняем индекс, чтобы менять картинки
        self.frame_index += 0.15
        self.image = self.frames[int(self.frame_index) % (len(self.frames) - 1)]

        # пермещаем врага
        self.move()

        # разворот картинок при необходимости
        # self.reverse_image()

    # пермещаем врага
    def move(self):
        self.rect.x += self.speed

#  def reverse_image(self):  # если бежит влево, то разворачиваем картинки
#      if self.speed < 0:
#          self.image = pygame.transform.flip(self.image, True, False)

    # вызываем в level, если наткнулся на ограничитель. меняем направление
    def reverse(self):
        self.speed *= -1
