import pygame


# класс кнопки
class Button:
    def __init__(self, text, position, width, height, color, hover_color, text_color, font_size):
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color  # Цвет при наведении
        self.text_color = text_color
        self.font_size = font_size  # Размер шрифта
        self.font = pygame.font.Font(None, self.font_size)  # шрифт по умолчанию указанного размера
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        self.hovered = False

    def draw(self, screen):
        if self.is_hovered(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self, mouse_pos):  # проверка наведения мыши на кнопку
        if self.rect.collidepoint(mouse_pos):
            return True
        return False