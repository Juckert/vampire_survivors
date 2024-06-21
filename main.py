import pygame
import sys
import random
from player import Player
from obstacle import Rock, Tree
from enemy import Knight

class Game:
    def __init__(self):
        self.init_game_settings()
        self.init_pygame()
        self.load_background()
        self.create_player()
        self.create_obstacles()
        self.create_enemies()
        self.setup_fps()

    def init_game_settings(self):
        self.WINDOW_WIDTH = 1440
        self.WINDOW_HEIGHT = 800
        self.MAP_WIDTH = 2880
        self.MAP_HEIGHT = 1600

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survivors")

    def load_background(self):
        self.background = pygame.image.load("images\\fon\\fon_2.jpg")
        self.background = pygame.transform.scale(self.background, (self.MAP_WIDTH, self.MAP_HEIGHT))

    def create_player(self):
        self.player = Player(self.MAP_WIDTH // 2, self.MAP_HEIGHT // 2, 5)
        self.camera_x = self.player.x - self.WINDOW_WIDTH // 2
        self.camera_y = self.player.y - self.WINDOW_HEIGHT // 2

    def create_obstacles(self):
        self.obstacles = []
        player_x = self.MAP_WIDTH // 2
        player_y = self.MAP_HEIGHT // 2
        avoid_radius = 100
        min_distance = 50
        occupied_positions = []

        def is_in_player_zone(x, y):
            return abs(x - player_x) < avoid_radius and abs(y - player_y) < avoid_radius

        def is_too_close_to_other_obstacles(x, y):
            for pos in occupied_positions:
                if abs(x - pos[0]) < min_distance and abs(y - pos[1]) < min_distance:
                    return True
            return False

        def is_valid_position(x, y):
            return not is_in_player_zone(x, y) and not is_too_close_to_other_obstacles(x, y)

        for _ in range(5):
            while True:
                x, y = random.randint(0, self.MAP_WIDTH - 75), random.randint(0, self.MAP_HEIGHT - 75)
                if is_valid_position(x, y):
                    occupied_positions.append((x, y))
                    break
            self.obstacles.append(Rock(x, y))

        tree_types = ["birch", "oak", "withered_tree", "withered_white_tree"]
        for _ in range(5):
            while True:
                x, y = random.randint(0, self.MAP_WIDTH - 75), random.randint(0, self.MAP_HEIGHT - 75)
                if is_valid_position(x, y):
                    occupied_positions.append((x, y))
                    break
            tree_type = random.choice(tree_types)
            self.obstacles.append(Tree(x, y, tree_type))

    def create_enemies(self):
        self.enemies = []
        for _ in range(3):
            while True:
                x, y = random.randint(0, self.MAP_WIDTH - 75), random.randint(0, self.MAP_HEIGHT - 75)
                if abs(x - self.player.x) > self.WINDOW_WIDTH // 2 or abs(y - self.player.y) > self.WINDOW_HEIGHT // 2:
                    break
            self.enemies.append(Knight(x, y))

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
        self.player.update(keys, self.MAP_WIDTH, self.MAP_HEIGHT, self.obstacles)
        for enemy in self.enemies:
            enemy.update(self.player.x, self.player.y, self.obstacles)
        self.update_camera()

    def update_camera(self):
        self.camera_x = self.player.x - self.WINDOW_WIDTH // 2
        self.camera_y = self.player.y - self.WINDOW_HEIGHT // 2

        self.camera_x = max(0, min(self.camera_x, self.MAP_WIDTH - self.WINDOW_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.MAP_HEIGHT - self.WINDOW_HEIGHT))

    def draw_frame(self):
        self.screen.blit(self.background, (-self.camera_x, -self.camera_y))  # Отрисовка фона
        for obstacle in self.obstacles:
            obstacle.draw(self.screen, self.camera_x, self.camera_y)
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x, self.camera_y)
        self.player.draw(self.screen, self.camera_x, self.camera_y)
        pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
