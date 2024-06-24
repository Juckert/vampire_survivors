import pygame

class BaseMenu:
    def __init__(self, screen, window_width, window_height, background_image):
        self._screen = screen
        self._window_width = window_width
        self._window_height = window_height
        self._background_image = background_image
        self._title_font = pygame.font.Font(None, 74)
        self._button_font = pygame.font.Font(None, 36)

    @property
    def screen(self):
        return self._screen

    @property
    def window_width(self):
        return self._window_width

    @property
    def window_height(self):
        return self._window_height

    @property
    def background_image(self):
        return self._background_image

    @property
    def title_font(self):
        return self._title_font

    @property
    def button_font(self):
        return self._button_font

    def draw_text_with_background(self, text, font, text_color, background_color, center):
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=center)
        background_rect = text_rect.inflate(10, 10)
        pygame.draw.rect(self._screen, background_color, background_rect)
        self._screen.blit(text_surface, text_rect)

    def draw_text_no_background(self, text, font, color, center):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center)
        self._screen.blit(text_surface, text_rect)

    def draw_background(self):
        self._screen.blit(self._background_image, (0, 0))

    def draw_button(self, rect, text, text_color, background_color):
        pygame.draw.rect(self._screen, background_color, rect)
        self.draw_text_with_background(text, self._button_font, text_color, background_color, rect.center)

    def update(self):
        pass

    def draw(self):
        pass

class Menu(BaseMenu):
    def __init__(self, screen, window_width, window_height, background_image):
        super().__init__(screen, window_width, window_height, background_image)
        self._play_button = pygame.Rect(window_width // 2 - 50, window_height // 2 - 25, 100, 50)

    def draw(self):
        self.draw_background()

        title_centers = [
            (self.window_width // 2, self.window_height // 2 - 350),
            (self.window_width // 2, self.window_height // 2 - 250)
        ]
        titles = ["Vampire", "Survivors"]
        for title, center in zip(titles, title_centers):
            self.draw_text_no_background(title, self.title_font, (255, 0, 0), center)
        
        self.draw_button(self._play_button, "Начать", (255, 255, 255), (0, 0, 255))
        
        pygame.display.flip()

class PauseMenu(BaseMenu):
    def __init__(self, screen, window_width, window_height, background_image):
        super().__init__(screen, window_width, window_height, background_image)
        button_width = 200
        button_height = 50
        button_x = window_width // 2 - button_width // 2
        self._continue_button = pygame.Rect(button_x, window_height // 2 - 50, button_width, button_height)
        self._quit_button = pygame.Rect(button_x, window_height // 2 + 50, button_width, button_height)

    def draw(self):
        self.draw_background()
        pause_center = (self.window_width // 2, self.window_height // 2 - 350)
        self.draw_text_no_background("Пауза", self.title_font, (255, 0, 0), pause_center)
        
        self.draw_button(self._continue_button, "Продолжить", (255, 255, 255), (0, 0, 255))
        self.draw_button(self._quit_button, "Выйти в меню", (255, 255, 255), (0, 0, 255))
        
        pygame.display.flip()

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._continue_button.collidepoint(event.pos):
                return "continue"
            elif self._quit_button.collidepoint(event.pos):
                return "quit"
        return None

class GameOverMenu(BaseMenu):
    def __init__(self, screen, window_width, window_height, background_image):
        super().__init__(screen, window_width, window_height, background_image)
        self._menu_button = pygame.Rect(window_width // 2 - 100, window_height // 2 + 50, 200, 50)

    def draw(self):
        self.draw_background()

        game_over_center = (self.window_width // 2, self.window_height // 2 - 350)
        self.draw_text_no_background("Game Over", self.title_font, (255, 0, 0), game_over_center)
        
        self.draw_button(self._menu_button, "Выйти в меню", (255, 255, 255), (0, 0, 255))
        
        pygame.display.flip()

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._menu_button.collidepoint(event.pos):
                return "menu"
        return None
