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
        background_rect = text_rect.inflate(10, 10)  # Extend background rectangle around text
        pygame.draw.rect(self.screen, background_color, background_rect)
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

        # Draw title text with black background and gold color
        title_text_center = (self.window_width // 2, self.window_height // 2 - 100)
        self.draw_text_with_background("Vampire Survivors", self.title_font, (255, 215, 0), (0, 0, 0), title_text_center)
        
        # Draw play button with black background and gold color
        pygame.draw.rect(self.screen, (0, 0, 0), self.play_button)
        play_text_center = self.play_button.center
        self.draw_text_with_background("Play", self.button_font, (255, 215, 0), (0, 0, 0), play_text_center)
        
        pygame.display.flip()


class PauseMenu(BaseMenu):
    def __init__(self, screen, window_width, window_height, background_image):
        super().__init__(screen, window_width, window_height, background_image)
        self.pause_font = pygame.font.Font(None, 74)

    def draw(self):
        self.draw_background()

        # Draw "Paused" text with black background and gold color
        self.draw_text_with_background("Paused", self.pause_font, (255, 215, 0), (0, 0, 0), (self.window_width // 2, self.window_height // 2))
        
        pygame.display.flip()


class GameOverMenu(BaseMenu):
    def __init__(self, screen, window_width, window_height, background_image):
        super().__init__(screen, window_width, window_height, background_image)
        self.menu_button = pygame.Rect(window_width // 2 - 100, window_height // 2 + 50, 200, 50)

    def draw(self):
        self.draw_background()

        # Draw "Game Over" text with black background and gold color
        self.draw_text_with_background("Game Over", self.title_font, (255, 215, 0), (0, 0, 0), (self.window_width // 2, self.window_height // 2 - 100))
        
        # Draw "Main Menu" button with black background and gold color
        pygame.draw.rect(self.screen, (0, 0, 0), self.menu_button)
        menu_text_center = self.menu_button.center
        self.draw_text_with_background("Main Menu", self.button_font, (255, 215, 0), (0, 0, 0), menu_text_center)
        
        pygame.display.flip()