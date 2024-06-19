import pygame
import sys
from player import Player

class Game:
    def __init__(self):
        self.init_game_settings()
        self.init_pygame()
        self.create_player()
        self.create_map()
        self.setup_fps()

    def init_game_settings(self):
        self.WINDOW_WIDTH = 1440
        self.WINDOW_HEIGHT = 800

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Черная карта и перемещение персонажа")

    def create_player(self):
        self.player = Player(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2, 5)

    def create_map(self):
        self.map_color = (0, 0, 0)  # Черный цвет

    def setup_fps(self):
        self.FPS = 30
        self.running = True
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            self.handle_events()
            self.update_game_state()
            self.draw_frame()
            self.clock.tick(self.FPS)
        self.quit_game()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update_game_state(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.screen)

    def draw_frame(self):
        self.screen.fill(self.map_color)
        self.player.draw(self.screen)
        pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
