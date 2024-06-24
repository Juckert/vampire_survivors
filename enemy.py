import pygame
from abc import ABC, abstractmethod
import time
import random

class Enemy(ABC):
    BASE_MIN_SPEED = 1
    BASE_MAX_SPEED = 5
    BASE_MIN_HP = 30
    BASE_MAX_HP = 70
    BASE_ATTACK_POWER = 5

    def __init__(self, x, y, speed_coeff, hp_coeff, attack_power_coeff, image_paths, hurt_image_path=None):
        self.x, self.y = x, y
        self.speed = random.randint(int(self.BASE_MIN_SPEED * speed_coeff), int(self.BASE_MAX_SPEED * speed_coeff))
        self.hp = random.randint(int(self.BASE_MIN_HP * hp_coeff), int(self.BASE_MAX_HP * hp_coeff))
        self.attack_power = int(self.BASE_ATTACK_POWER * attack_power_coeff)
        self.images_right = self.load_images(image_paths)
        self.images_left = [pygame.transform.flip(image, True, False) for image in self.images_right]
        self.current_sprite, self.is_facing_left = 0, False
        self.rect = pygame.Rect(self.x, self.y, 75, 75)
        self.last_attack_time = 0
        self.hurt = False
        self.hurt_start_time = 0
        self.hurt_image_right = None
        self.hurt_image_left = None
        if hurt_image_path:
            self.hurt_image_right = pygame.transform.scale(pygame.image.load(hurt_image_path), (75, 75))
            self.hurt_image_left = pygame.transform.flip(self.hurt_image_right, True, False)

    def load_images(self, paths):
        return [pygame.transform.scale(pygame.image.load(path), (75, 75)) for path in paths]

    def update_position(self, player_x, player_y):
        prev_x, prev_y = self.x, self.y

        if abs(self.x - player_x) > abs(self.y - player_y):
            if self.x < player_x:
                self.x += self.speed
                self.is_facing_left = False
            else:
                self.x -= self.speed
                self.is_facing_left = True
        else:
            if self.y < player_y:
                self.y += self.speed
            else:
                self.y -= self.speed

        self.rect.topleft = (self.x, self.y)
        return prev_x, prev_y

    def handle_collisions(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                return True
        return False

    def attack_player(self, player):
        current_time = time.time()
        if self.rect.colliderect(player.rect) and current_time - self.last_attack_time >= 1:
            player.take_damage(self.attack_power)
            self.last_attack_time = current_time

    def update(self, player_x, player_y, player, obstacles):
        prev_x, prev_y = self.update_position(player_x, player_y)

        if self.handle_collisions(obstacles):
            self.x, self.y = prev_x, prev_y
            self.rect.topleft = (self.x, self.y)

        self.attack_player(player)

        if self.hurt and time.time() - self.hurt_start_time > 1:  # Восстановление после 1 секунды
            self.hurt = False

    def draw(self, screen, camera_x, camera_y):
        if self.hurt:
            image = self.hurt_image_left if self.is_facing_left else self.hurt_image_right
        else:
            images = self.images_left if self.is_facing_left else self.images_right
            image = images[int(self.current_sprite)]
            self.current_sprite = (self.current_sprite + 0.08) % len(images)
        screen.blit(image, (self.x - camera_x, self.y - camera_y))

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        self.hurt = True
        self.hurt_start_time = time.time()

class Knight(Enemy):
    def __init__(self, x, y):
        speed_coeff = random.uniform(1, 1.2)
        hp_coeff = random.uniform(1, 1.5)
        attack_power_coeff = random.uniform(1.3, 1.6)
        image_paths = [f"images/enemies/Knight/Run/Knight_Run_{i}.png" for i in range(1, 9)]
        hurt_image_path = "images/enemies/Knight/Hurt/Knight_hurt.png"
        super().__init__(x, y, speed_coeff, hp_coeff, attack_power_coeff, image_paths, hurt_image_path)

class Skeleton(Enemy):
    def __init__(self, x, y):
        speed_coeff = random.uniform(1.1, 1.4)
        hp_coeff = random.uniform(0.5, 0.8)
        attack_power_coeff = random.uniform(0.8, 1.3)
        image_paths = [f"images/enemies/Skeleton/Run/Skeleton_Run_{i}.png" for i in range(1, 13)]
        hurt_image_path = "images/enemies/Skeleton/Hurt/Skeleton_Hurt.png"
        super().__init__(x, y, speed_coeff, hp_coeff, attack_power_coeff, image_paths, hurt_image_path)

class Demon(Enemy):
    def __init__(self, x, y):
        speed_coeff = random.uniform(1.2, 1.5)
        hp_coeff = random.uniform(1, 1.5)
        attack_power_coeff = random.uniform(1, 1.5)
        image_paths = [f"images\enemies\Demon\Run\Demon_Run_{i}.png" for i in range(1, 9)]
        hurt_image_path = "images\enemies\Demon\Hurt\Demon_Hurt.png"
        super().__init__(x, y, speed_coeff, hp_coeff, attack_power_coeff, image_paths, hurt_image_path)
