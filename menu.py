import pygame

class BaseMenu:
    def __init__(self, screen, window_width, window_height, background_image):
        self.screen = screen
        self.window_width = window_width
        self.window_height = window_height
        self.background_image = background_image
        self.title_font = pygame.font.Font(None, 74)
        self.button_font = pygame.font.Font(None, 36)

    def draw_text_with_background(self, text, font, text_color, background_color, center):
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=center)
        background_rect = text_rect.inflate(10, 10)
        pygame.draw.rect(self.screen, background_color, background_rect)
        self.screen.blit(text_surface, text_rect)

    def draw_text_no_background(self, text, font, color, center):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center)
        self.screen.blit(text_surface, text_rect)

    def draw_background(self):
        self.screen.blit(self.background_image, (0, 0))

    def update(self):
        pass

    def draw(self):
        pass

class Menu(BaseMenu):
    def __init__(self, screen, window_width, window_height, background_image):
        super().__init__(screen, window_width, window_height, background_image)
        self.play_button = pygame.Rect(window_width // 2 - 50, window_height // 2 - 25, 100, 50)

    def draw(self):
        self.draw_background()

        first_part_center = (self.window_width // 2, self.window_height // 2 - 350)
        self.draw_text_no_background("Vampire", self.title_font, (255, 0, 0), first_part_center)
        
        second_part_center = (self.window_width // 2, self.window_height // 2 - 250)
        self.draw_text_no_background("Survivors", self.title_font, (255, 0, 0), second_part_center)
        
        pygame.draw.rect(self.screen, (0, 0, 255), self.play_button)
        play_text_center = self.play_button.center
        self.draw_text_with_background("Начать", self.button_font, (255, 255, 255), (0, 0, 255), play_text_center)
        
        pygame.display.flip()

class PauseMenu(BaseMenu):
    def __init__(self, screen, window_width, window_height, background_image):
        super().__init__(screen, window_width, window_height, background_image)
        self.pause_font = pygame.font.Font(None, 74)
        button_width = 200
        button_height = 50
        button_x = window_width // 2 - button_width // 2
        self.continue_button = pygame.Rect(button_x, window_height // 2 - 50, button_width, button_height)
        self.quit_button = pygame.Rect(button_x, window_height // 2 + 50, button_width, button_height)

    def draw(self):
        self.draw_background()
        pause_center = (self.window_width // 2, self.window_height // 2 - 350)
        self.draw_text_no_background("Пауза", self.pause_font, (255, 0, 0), pause_center)
        
        pygame.draw.rect(self.screen, (0, 0, 255), self.continue_button)
        continue_text_center = self.continue_button.center
        self.draw_text_with_background("Продолжить", self.button_font, (255, 255, 255), (0, 0, 255), continue_text_center)
        
        pygame.draw.rect(self.screen, (0, 0, 255), self.quit_button)
        quit_text_center = self.quit_button.center
        self.draw_text_with_background("Выйти в меню", self.button_font, (255, 255, 255), (0, 0, 255), quit_text_center)
        
        pygame.display.flip()

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.continue_button.collidepoint(event.pos):
                return "continue"
            elif self.quit_button.collidepoint(event.pos):
                return "quit"
        return None

class GameOverMenu(BaseMenu):
    def __init__(self, screen, window_width, window_height, background_image):
        super().__init__(screen, window_width, window_height, background_image)
        self.menu_button = pygame.Rect(window_width // 2 - 100, window_height // 2 + 50, 200, 50)

    def draw(self):
        self.draw_background()

        game_over_center = (self.window_width // 2, self.window_height // 2 - 350)
        self.draw_text_no_background("Game Over", self.title_font, (255, 0, 0), game_over_center)
        
        pygame.draw.rect(self.screen, (0, 0, 255), self.menu_button)
        menu_text_center = self.menu_button.center
        self.draw_text_with_background("Выйти в меню", self.button_font, (255, 255, 255), (0, 0, 255), menu_text_center)
        
        pygame.display.flip()

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_button.collidepoint(event.pos):
                return "menu"
        return None
