import pygame
import sys
import random
import time
from player import Punk
from obstacle import Rock, Tree
from enemy import Knight, Skeleton

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
        self.defeated_enemies = 0
        self.menu = Menu(self.screen, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.pause_menu = PauseMenu(self.screen, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.game_over_menu = GameOverMenu(self.screen, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.start_time = None
        self.start_game()  # Start game setup

    def start_game(self):
        self.defeated_enemies = 0
        self.background = self.load_background()
        self.player = Punk(self.MAP_WIDTH // 2, self.MAP_HEIGHT // 2, 5)
        self.camera_x = self.player.x - self.WINDOW_WIDTH // 2
        self.camera_y = self.player.y - self.WINDOW_HEIGHT // 2
        self.obstacles = self.create_obstacles()
        self.enemies = self.create_enemies()
        self.start_time = pygame.time.get_ticks()

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
                    enemy_type = random.choice([Knight, Skeleton])
                    enemies.append(enemy_type(x, y))
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
            elif self.state == "paused":
                self.handle_pause_events()
                self.pause_menu.draw()
            elif self.state == "game_over":
                self.handle_game_over_events()
                self.game_over_menu.draw()
            self.clock.tick(self.FPS)
        self.quit_game()

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu.play_button.collidepoint(event.pos):
                    self.start_game()  # Reset the game state
                    self.state = "playing"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.state = "paused"

    def handle_pause_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.state = "playing"
                elif event.key == pygame.K_q:
                    self.state = "menu"

    def update_game_state(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.MAP_WIDTH, self.MAP_HEIGHT, self.obstacles)
        self.update_enemies()
        self.update_camera()

        # Calculate the elapsed time in seconds
        current_time = pygame.time.get_ticks()
        self.elapsed_time = (current_time - self.start_time) / 1000

        if self.player.hp <= 0:
            self.state = "game_over"

    def update_enemies(self):
        for enemy in self.enemies[:]:
            enemy.update(self.player.x, self.player.y, self.player, self.obstacles)
            for fireball in self.player.fireballs[:]:
                if fireball.rect.colliderect(enemy.rect):
                    enemy.take_damage(self.player.attack_power)
                    self.player.fireballs.remove(fireball)
                    if enemy.hp <= 0:
                        self.enemies.remove(enemy)
                        self.defeated_enemies += 1  # Increment defeated enemies counter
                    break

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

        # Render the elapsed time
        self.draw_timer()
        self.draw_defeated_enemies()
        pygame.display.flip()
    
    def draw_timer(self):
        font = pygame.font.Font(None, 50)
        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)      
        time_text = font.render(f"{minutes:02}:{seconds:02}", True, (255, 255, 255))
        self.screen.blit(time_text, (self.screen.get_width() // 2 - 50, 20))

    def handle_game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over_menu.menu_button.collidepoint(event.pos):
                    self.state = "menu"
                    
    def draw_defeated_enemies(self):
        skull_image = pygame.image.load("images/decor/Skull.png")
        skull_image = pygame.transform.scale(skull_image, (40, 40))
        skull_rect = skull_image.get_rect()
        skull_x = self.WINDOW_WIDTH - skull_rect.width - 10
        skull_y = 10
        self.screen.blit(skull_image, (skull_x, skull_y))

        font = pygame.font.Font(None, 36)
        text = font.render(str(self.defeated_enemies), True, (255, 255, 255))  # White color
        text_rect = text.get_rect(midright=(skull_x - 5, skull_y + skull_rect.height // 2))
        self.screen.blit(text, text_rect)

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

class PauseMenu:
    def __init__(self, screen, window_width, window_height):
        self.screen = screen
        self.window_width = window_width
        self.window_height = window_height
        self.font = pygame.font.Font(None, 74)

    def draw(self):
        self.screen.fill((0, 0, 0))
        pause_text = self.font.render("Paused", True, (255, 255, 255))
        self.screen.blit(pause_text, (self.window_width // 2 - 100, self.window_height // 2 - 100))
        resume_text = self.font.render("Press P to Resume", True, (255, 255, 255))
        self.screen.blit(resume_text, (self.window_width // 2 - 250, self.window_height // 2))
        quit_text = self.font.render("Press Q to Quit", True, (255, 255, 255))
        self.screen.blit(quit_text, (self.window_width // 2 - 200, self.window_height // 2 + 100))
        pygame.display.flip()

class GameOverMenu:
    def __init__(self, screen, window_width, window_height):
        self.screen = screen
        self.window_width = window_width
        self.window_height = window_height
        self.font = pygame.font.Font(None, 74)
        self.menu_button = pygame.Rect((window_width // 2 - 100, window_height // 2 - 50), (200, 100))

    def draw(self):
        self.screen.fill((0, 0, 0))
        game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        self.screen.blit(game_over_text, (self.window_width // 2 - 150, self.window_height // 2 - 100))
        menu_text = self.font.render("Menu", True, (255, 255, 255))
        self.screen.blit(menu_text, (self.menu_button.x + 50, self.menu_button.y + 25))
        pygame.draw.rect(self.screen, (255, 255, 255), self.menu_button, 2)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()