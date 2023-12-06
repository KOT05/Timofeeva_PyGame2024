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


# главное меню
def main_menu(screen):
    start_button = Button('Играть', (250, 150), 150, 50, 'green', 'red', 'purple', 40)
    settings_button = Button('Настройки', (250, 210), 150, 50, 'green', 'red', 'purple', 40)
    exit_button = Button('Выход', (250, 270), 150, 50, 'green', 'red', 'purple', 40)

    running = True
    while running:
        screen.fill((0, 0, 0))
        main_background = pygame.image.load('Resources\Images\dream_TradingCard.jpg')
        main_background = pygame.transform.scale(main_background, (640, 480))
        screen.blit(main_background, (0, 0))
        start_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)

        font = pygame.font.Font(None, 80)
        text_surface = font.render("Побег", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(320, 100))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_hovered(event.pos):
                    # start
                    pass
                elif exit_button.is_hovered(event.pos):
                    running = False
                elif settings_button.is_hovered(event.pos):
                    pass
        pygame.display.flip()


# pygame.init()
# size = width, height = 640, 480
# screen = pygame.display.set_mode(size)
# main_menu(screen)
