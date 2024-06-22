import pygame
import sys
import random
from player import Player
from obstacle import Rock, Tree
from enemy import Knight

class Game:
    WINDOW_WIDTH = 1440
    WINDOW_HEIGHT = 800
    MAP_WIDTH = 2880
    MAP_HEIGHT = 1600
    FPS = 30

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survivors")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"  # Initial state set to 'menu'
        
        self.background = self.load_background()
        self.player = Player(self.MAP_WIDTH // 2, self.MAP_HEIGHT // 2, 5)
        self.camera_x = self.player.x - self.WINDOW_WIDTH // 2
        self.camera_y = self.player.y - self.WINDOW_HEIGHT // 2
        self.obstacles = self.create_obstacles()
        self.enemies = self.create_enemies()  # Generate enemies with random count

        self.menu = Menu(self.screen, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

    def load_background(self):
        background = pygame.image.load("images/fon/fon_2.jpg")
        return pygame.transform.scale(background, (self.MAP_WIDTH, self.MAP_HEIGHT))

    def create_obstacles(self):
        obstacles = []
        player_x, player_y = self.MAP_WIDTH // 2, self.MAP_HEIGHT // 2
        occupied_positions = set()
        avoid_radius, min_distance = 100, 400

        def is_valid_position(x, y):
            if abs(x - player_x) < avoid_radius and abs(y - player_y) < avoid_radius:
                return False
            for ox, oy in occupied_positions:
                if abs(x - ox) < min_distance and abs(y - oy) < min_distance:
                    return False
            return True

        for _ in range(5):
            x, y = self.get_random_position(is_valid_position)
            occupied_positions.add((x, y))
            obstacles.append(Rock(x, y))

        tree_types = ["birch", "oak", "withered_tree", "withered_white_tree"]
        for _ in range(5):
            x, y = self.get_random_position(is_valid_position)
            occupied_positions.add((x, y))
            obstacles.append(Tree(x, y, random.choice(tree_types)))

        return obstacles

    def get_random_position(self, is_valid_position):
        while True:
            x, y = random.randint(0, self.MAP_WIDTH - 75), random.randint(0, self.MAP_HEIGHT - 75)
            if is_valid_position(x, y):
                return x, y

    def create_enemies(self):
        enemies = []
        num_enemies = random.randint(5, 10)  # Random number of enemies between 5 and 10
        for _ in range(num_enemies):
            while True:
                x, y = random.randint(0, self.MAP_WIDTH - 75), random.randint(0, self.MAP_HEIGHT - 75)
                if abs(x - self.player.x) > self.WINDOW_WIDTH // 2 or abs(y - self.player.y) > self.WINDOW_HEIGHT // 2:
                    enemies.append(Knight(x, y))
                    break
        return enemies

    def run(self):
        while self.running:
            if self.state == "menu":
                self.menu.update()
                self.menu.draw()
                self.handle_menu_events()
            elif self.state == "playing":
                self.handle_events()
                self.update_game_state()
                self.draw_frame()
            self.clock.tick(self.FPS)
        self.quit_game()

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu.play_button.collidepoint(event.pos):
                    self.state = "playing"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update_game_state(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.MAP_WIDTH, self.MAP_HEIGHT, self.obstacles)
        self.update_enemies()
        self.update_camera()

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update(self.player.x, self.player.y, self.player, self.obstacles)

    def update_camera(self):
        self.camera_x = max(0, min(self.player.x - self.WINDOW_WIDTH // 2, self.MAP_WIDTH - self.WINDOW_WIDTH))
        self.camera_y = max(0, min(self.player.y - self.WINDOW_HEIGHT // 2, self.MAP_HEIGHT - self.WINDOW_HEIGHT))

    def draw_frame(self):
        self.screen.blit(self.background, (-self.camera_x, -self.camera_y))
        for obstacle in self.obstacles:
            obstacle.draw(self.screen, self.camera_x, self.camera_y)
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x, self.camera_y)
        self.player.draw(self.screen, self.camera_x, self.camera_y)
        pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        sys.exit()

class Menu:
    def __init__(self, screen, window_width, window_height):
        self.screen = screen
        self.window_width = window_width
        self.window_height = window_height
        self.font = pygame.font.Font(None, 74)
        self.play_button = pygame.Rect((window_width // 2 - 100, window_height // 2 - 50), (200, 100))

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        play_text = self.font.render("Play", True, (255, 255, 255))
        self.screen.blit(play_text, (self.play_button.x + 50, self.play_button.y + 25))
        pygame.draw.rect(self.screen, (255, 255, 255), self.play_button, 2)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
