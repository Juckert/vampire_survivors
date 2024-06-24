import pygame
import sys
import random
from player import Punk, Cyborg
from obstacle import Rock, Tree
from enemy import Knight, Skeleton, Demon
from menu import Menu, PauseMenu, GameOverMenu

class Game:
    WINDOW_WIDTH = 1440
    WINDOW_HEIGHT = 800
    MAP_WIDTH = 2880
    MAP_HEIGHT = 1600
    FPS = 30

    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survivors")
        self._clock = pygame.time.Clock()
        self._running = True
        self._state = "menu"
        self._defeated_enemies = 0
        self._background_image = self._load_background_image()  # Load background image for menus
        self._menu = Menu(self._screen, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self._background_image)
        self._pause_menu = PauseMenu(self._screen, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self._background_image)
        self._game_over_menu = GameOverMenu(self._screen, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self._background_image)
        self._start_time = None
        self._pause_start_time = None
        self._total_paused_time = 0
        self._start_game()

    def _start_game(self):
        self._defeated_enemies = 0
        self._background = self._load_background()
        self._player = Punk(self.MAP_WIDTH // 2, self.MAP_HEIGHT // 2)
        self._camera_x = self._player.x - self.WINDOW_WIDTH // 2
        self._camera_y = self._player.y - self.WINDOW_HEIGHT // 2
        self._obstacles = self._create_obstacles()
        self._enemies = self._create_enemies()
        self._start_time = pygame.time.get_ticks()

    def _load_background_image(self):
        image = pygame.image.load("images/fon/Blood_moon.jpg")
        return pygame.transform.scale(image, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

    def _load_background(self):
        background = pygame.image.load("images/fon/fon_2.jpg")
        return pygame.transform.scale(background, (self.MAP_WIDTH, self.MAP_HEIGHT))

    def _create_obstacles(self):
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
            x, y = self._get_random_position(is_valid_position)
            occupied_positions.add((x, y))
            obstacles.append(Rock(x, y))

        tree_types = ["birch", "oak", "withered_tree", "withered_white_tree"]
        for _ in range(5):
            x, y = self._get_random_position(is_valid_position)
            occupied_positions.add((x, y))
            obstacles.append(Tree(x, y, random.choice(tree_types)))

        return obstacles

    def _get_random_position(self, is_valid_position):
        while True:
            x, y = random.randint(0, self.MAP_WIDTH - 75), random.randint(0, self.MAP_HEIGHT - 75)
            if is_valid_position(x, y):
                return x, y

    def _is_valid_enemy_spawn_position(self, x, y):
        if abs(x - self._player.x) <= self.WINDOW_WIDTH // 2 and abs(y - self._player.y) <= self.WINDOW_HEIGHT // 2:
            return False
        if self._is_visible_to_player(x, y):
            return False
        if not self._is_valid_enemy_position(x, y):
            return False
        return True

    def _is_valid_enemy_position(self, x, y):
        safe_distance = 150
        for obstacle in self._obstacles:
            if obstacle.rect.collidepoint(x, y):
                return False
            if abs(x - obstacle.rect.centerx) < safe_distance and abs(y - obstacle.rect.centery) < safe_distance:
                return False
        return True

    def _is_visible_to_player(self, x, y):
        player_rect = pygame.Rect(
            self._player.x - self.WINDOW_WIDTH // 2,
            self._player.y - self.WINDOW_HEIGHT // 2,
            self.WINDOW_WIDTH,
            self.WINDOW_HEIGHT
        )
        return player_rect.collidepoint(x, y)

    def _create_enemies(self):
        enemies = []
        num_enemies = random.randint(20, 30)
        for _ in range(num_enemies):
            enemies.append(self._spawn_enemy())
        return enemies

    def _spawn_enemy(self):
        while True:
            x, y = random.randint(0, self.MAP_WIDTH - 75), random.randint(0, self.MAP_HEIGHT - 75)
            if self._is_valid_enemy_spawn_position(x, y):
                enemy_type = random.choice([Knight, Skeleton, Demon])
                break
        return enemy_type(x, y)

    def run(self):
        while self._running:
            if self._state == "menu":
                self._menu.update()
                self._menu.draw()
                for event in pygame.event.get():
                    self._handle_menu_events(event)
            elif self._state == "playing":
                self._handle_events()
                self._update_game_state()
                self._draw_frame()
            elif self._state == "paused":
                self._pause_menu.draw(self._elapsed_time, self._defeated_enemies)
                for event in pygame.event.get():
                    self._handle_pause_events(event)
            elif self._state == "game_over":
                self._game_over_menu.draw(self._elapsed_time, self._defeated_enemies)
                for event in pygame.event.get():
                    self._handle_game_over_events(event)

            self._clock.tick(self.FPS)
        self._quit_game()

    def _handle_menu_events(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self._menu._play_button.collidepoint(event.pos):
                self._start_game()
                self._state = "playing"
                self._total_paused_time = 0  # Reset paused time

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._state = "paused"
                    self._pause_start_time = pygame.time.get_ticks()
                elif event.key == pygame.K_LEFT:
                    self._player.move_left()
                elif event.key == pygame.K_RIGHT:
                    self._player.move_right()
                elif event.key == pygame.K_UP:
                    self._player.move_up()
                elif event.key == pygame.K_DOWN:
                    self._player.move_down()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self._player.stop_horizontal()
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self._player.stop_vertical()

    def _handle_pause_events(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._state = "playing"
                self._total_paused_time += pygame.time.get_ticks() - self._pause_start_time
        elif event.type == pygame.MOUSEBUTTONDOWN:
            action = self._pause_menu.handle_events(event)
            if action == "continue":
                self._state = "playing"
                self._total_paused_time += pygame.time.get_ticks() - self._pause_start_time
            elif action == "quit":
                self._state = "menu"

    def _update_game_state(self):
        keys = pygame.key.get_pressed()
        self._player.update(keys, self.MAP_WIDTH, self.MAP_HEIGHT, self._obstacles)
        self._update_enemies()
        self._update_camera()

        current_time = pygame.time.get_ticks()
        self._elapsed_time = (current_time - self._start_time - self._total_paused_time) / 1000

        if self._player.hp <= 0:
            self._state = "game_over"

    def _update_enemies(self):
        for enemy in self._enemies[:]:
            enemy.update(self._player.x, self._player.y, self._player, self._obstacles)
            for fireball in self._player._fireballs[:]:
                if fireball.rect.colliderect(enemy._rect):
                    enemy.take_damage(self._player.attack_power)
                    self._player._fireballs.remove(fireball)
                    if enemy.hp <= 0:
                        self._enemies.remove(enemy)
                        self._defeated_enemies += 1
                        new_enemy = self._spawn_enemy()
                        self._enemies.append(new_enemy)
                    break

    def _update_camera(self):
        self._camera_x = max(0, min(self._player.x - self.WINDOW_WIDTH // 2, self.MAP_WIDTH - self.WINDOW_WIDTH))
        self._camera_y = max(0, min(self._player.y - self.WINDOW_HEIGHT // 2, self.MAP_HEIGHT - self.WINDOW_HEIGHT))

    def _draw_frame(self):
        self._screen.blit(self._background, (-self._camera_x, -self._camera_y))
        for obstacle in self._obstacles:
            obstacle.draw(self._screen, self._camera_x, self._camera_y)
        for enemy in self._enemies:
            enemy.draw(self._screen, self._camera_x, self._camera_y)
        self._player.draw(self._screen, self._camera_x, self._camera_y)

        self._draw_timer()
        self._draw_defeated_enemies()
        pygame.display.flip()

    def _draw_timer(self):
        font = pygame.font.Font(None, 50)
        minutes = int(self._elapsed_time // 60)
        seconds = int(self._elapsed_time % 60)
        time_text = font.render(f"{minutes:02}:{seconds:02}", True, (255, 255, 255))
        self._screen.blit(time_text, (self._screen.get_width() // 2 - 50, 20))

    def _handle_game_over_events(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self._game_over_menu._menu_button.collidepoint(event.pos):
                self._state = "menu"

    def _draw_defeated_enemies(self):
        skull_image = pygame.image.load("images/decor/Skull.png")
        skull_image = pygame.transform.scale(skull_image, (40, 40))
        skull_rect = skull_image.get_rect()
        skull_x = self.WINDOW_WIDTH - skull_rect.width - 10
        skull_y = 10
        self._screen.blit(skull_image, (skull_x, skull_y))

        font = pygame.font.Font(None, 36)
        text = font.render(str(self._defeated_enemies), True, (255, 255, 255))
        text_rect = text.get_rect(midright=(skull_x - 5, skull_y + skull_rect.height // 2))
        self._screen.blit(text, text_rect)

    def _quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
