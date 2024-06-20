import pygame
import sys
import random
from player import Player
from obstacle import Rock, Tree

class Game:
    def __init__(self):
        self.init_game_settings()
        self.init_pygame()
        self.load_background()
        self.create_player()
        self.create_obstacles()
        self.setup_fps()

    def init_game_settings(self):
        self.WINDOW_WIDTH = 1440
        self.WINDOW_HEIGHT = 800

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survivors")

    def load_background(self):
        self.background = pygame.image.load("images\\fon\\fon_2.jpg")
        self.background = pygame.transform.scale(self.background, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

    def create_player(self):
        self.player = Player(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2, 5)

    def create_obstacles(self):
        self.obstacles = []
        player_x = self.WINDOW_WIDTH // 2
        player_y = self.WINDOW_HEIGHT // 2
        avoid_radius = 100

        def is_in_player_zone(x, y):
            return abs(x - player_x) < avoid_radius and abs(y - player_y) < avoid_radius

        for _ in range(5):
            while True:
                x, y = random.randint(0, self.WINDOW_WIDTH - 75), random.randint(0, self.WINDOW_HEIGHT - 75)
                if not is_in_player_zone(x, y):
                    break
            self.obstacles.append(Rock(x, y))
        
        tree_types = ["birch", "oak", "withered_tree", "withered_white_tree"]
        for _ in range(5):
            while True:
                x, y = random.randint(0, self.WINDOW_WIDTH - 75), random.randint(0, self.WINDOW_HEIGHT - 75)
                if not is_in_player_zone(x, y):
                    break
            tree_type = random.choice(tree_types)
            self.obstacles.append(Tree(x, y, tree_type))

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
        self.player.update(keys, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.obstacles)

    def draw_frame(self):
        self.screen.blit(self.background, (0, 0))  # Отрисовка фона
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
    