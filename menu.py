import pygame
from abc import ABC, abstractmethod

# Базовый класс для всех меню
class BaseMenu(ABC):
    def __init__(self, screen, window_width, window_height, background_image):
        self._screen = screen
        self._window_width = window_width
        self._window_height = window_height
        self._background_image = background_image
        self._title_font = pygame.font.Font(None, 74)
        self._button_font = pygame.font.Font(None, 36)

    # Свойства для доступа к атрибутам
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
        ''' Метод для отрисовки текста с фоном '''
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=center)
        background_rect = text_rect.inflate(10, 10)
        pygame.draw.rect(self._screen, background_color, background_rect)
        self._screen.blit(text_surface, text_rect)

    def draw_text_no_background(self, text, font, color, center):
        ''' Метод для отрисовки текста без фона '''
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center)
        self._screen.blit(text_surface, text_rect)

    # Метод для отрисовки фона
    def draw_background(self):
        ''' Метод для отрисовки фона '''
        self._screen.blit(self._background_image, (0, 0))

    def draw_button(self, rect, text, text_color, background_color):
        ''' Метод для отрисовки кнопки '''
        pygame.draw.rect(self._screen, background_color, rect)
        self.draw_text_with_background(text, self._button_font, text_color, background_color, rect.center)

    def update(self):
        pass

    def draw(self):
        pass
    
    def handle_events(self, event):
        pass
    
class Menu(BaseMenu):
    ''' Класс меню игры, наследующийся от базового меню '''
    def __init__(self, screen, window_width, window_height, background_image):
        super().__init__(screen, window_width, window_height, background_image)
        self._play_button = pygame.Rect(window_width // 2 - 50, window_height // 2 + 50, 100, 50)
        self._punk_button = pygame.Rect(window_width // 2 - 150, window_height // 2 - 25, 100, 50)
        self._cyborg_button = pygame.Rect(window_width // 2 + 50, window_height // 2 - 25, 100, 50)
        self._selected_character = None

    def draw(self):
        ''' Метод для отрисовки меню '''
        self.draw_background()

        title_centers = [
            (self.window_width // 2, self.window_height // 2 - 350),
            (self.window_width // 2, self.window_height // 2 - 250)
        ]
        titles = ["Vampire", "Survivors"]
        for title, center in zip(titles, title_centers):
            self.draw_text_no_background(title, self.title_font, (255, 0, 0), center)
        
        self.draw_button(self._play_button, "Начать", (255, 255, 255), (0, 0, 255))
        self.draw_button(self._punk_button, "Punk", (255, 255, 255), (0, 0, 255))
        self.draw_button(self._cyborg_button, "Cyborg", (255, 255, 255), (0, 0, 255))
        
        pygame.display.flip()

    def handle_events(self, event):
        ''' Метод для обработки событий '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._play_button.collidepoint(event.pos):
                if self._selected_character == "Punk":
                    return "punk"
                elif self._selected_character == "Cyborg":
                    return "cyborg"
                else:
                    return "default"
            elif self._punk_button.collidepoint(event.pos):
                self._selected_character = "Punk"
            elif self._cyborg_button.collidepoint(event.pos):
                self._selected_character = "Cyborg"
        return None

class PauseMenu(BaseMenu):
    ''' Класс меню паузы, наследующийся от базового меню '''
    def __init__(self, screen, window_width, window_height, background_image):
        super().__init__(screen, window_width, window_height, background_image)
        button_width = 200
        button_height = 50
        button_x = window_width // 2 - button_width // 2
        self._continue_button = pygame.Rect(button_x, window_height // 2 - 50, button_width, button_height)
        self._quit_button = pygame.Rect(button_x, window_height // 2 + 50, button_width, button_height)

    def draw(self, elapsed_time, defeated_enemies):
        ''' Метод для отрисовки меню паузы '''
        self.draw_background()
        pause_center = (self.window_width // 2, self.window_height // 2 - 350)
        self.draw_text_no_background("Пауза", self.title_font, (255, 0, 0), pause_center)
        
        font = pygame.font.Font(None, 36)
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_text = f"Time: {minutes:02}:{seconds:02}"
        time_center = (self.window_width // 2, self.window_height // 2 - 250)
        self.draw_text_no_background(time_text, font, (255, 255, 255), time_center)
        
        enemies_text = f"Defeated Enemies: {defeated_enemies}"
        enemies_center = (self.window_width // 2, self.window_height // 2 - 200)
        self.draw_text_no_background(enemies_text, font, (255, 255, 255), enemies_center)
        
        self.draw_button(self._continue_button, "Продолжить", (255, 255, 255), (0, 0, 255))
        self.draw_button(self._quit_button, "Выйти в меню", (255, 255, 255), (0, 0, 255))
        
        pygame.display.flip()

    def handle_events(self, event):
        ''' Метод для обработки событий '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._continue_button.collidepoint(event.pos):
                return "continue"
            elif self._quit_button.collidepoint(event.pos):
                return "quit"
        return None

class GameOverMenu(BaseMenu):
    ''' Класс меню окончания игры, наследующийся от базового меню '''
    def __init__(self, screen, window_width, window_height, background_image):
        super().__init__(screen, window_width, window_height, background_image)
        self._menu_button = pygame.Rect(window_width // 2 - 100, window_height // 2 + 50, 200, 50)

    def draw(self, elapsed_time, defeated_enemies):
        ''' Метод для отрисовки меню окончания игры'''
        self.draw_background()

        game_over_center = (self.window_width // 2, self.window_height // 2 - 350)
        self.draw_text_no_background("Game Over", self.title_font, (255, 0, 0), game_over_center)
        
        font = pygame.font.Font(None, 50)
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_text = f"Time: {minutes:02}:{seconds:02}"
        time_center = (self.window_width // 2, self.window_height // 2 - 200)
        self.draw_text_no_background(time_text, font, (255, 255, 255), time_center)
        
        enemies_text = f"Defeated Enemies: {defeated_enemies}"
        enemies_center = (self.window_width // 2, self.window_height // 2 - 150)
        self.draw_text_no_background(enemies_text, font, (255, 255, 255), enemies_center)
        
        self.draw_button(self._menu_button, "Выйти в меню", (255, 255, 255), (0, 0, 255))
        
        pygame.display.flip()

    def handle_events(self, event):
        ''' Метод для обработки событий '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._menu_button.collidepoint(event.pos):
                return "menu"
        return None
