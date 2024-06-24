import pygame
from abc import ABC, abstractmethod
import time
import random

class Enemy(ABC):
    def __init__(self, x, y, speed, image_paths, hp, attack_power, hurt_image_path=None):
        self.x, self.y = x, y
        self.speed = speed
        self.hp, self.attack_power = hp, attack_power
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

    @abstractmethod
    def update(self, player_x, player_y, player, obstacles):
        pass

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
    MIN_SPEED = 1
    MAX_SPEED = 5
    MIN_HP = 30
    MAX_HP = 70

    def __init__(self, x, y):
        image_paths = [f"images/enemies/Knight/Run/Knight_Run_{i}.png" for i in range(1, 9)]
        hurt_image_path = "images/enemies/Knight/Hurt/Knight_hurt.png"
        speed = random.randint(self.MIN_SPEED, self.MAX_SPEED)
        hp = random.randint(self.MIN_HP, self.MAX_HP)
        super().__init__(x, y, speed, image_paths, hp, attack_power=5, hurt_image_path=hurt_image_path)

    def update(self, player_x, player_y, player, obstacles):
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

        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.x, self.y = prev_x, prev_y
                self.rect.topleft = (self.x, self.y)
                break

        if self.rect.colliderect(player.rect):
            current_time = time.time()
            if current_time - self.last_attack_time >= 1:
                player.take_damage(self.attack_power)
                self.last_attack_time = current_time

        if self.hurt and time.time() - self.hurt_start_time > 1:  # Восстановление после 1 секунды
            self.hurt = False

class Skeleton(Enemy):
    MIN_SPEED = 2
    MAX_SPEED = 6
    MIN_HP = 20
    MAX_HP = 50

    def __init__(self, x, y):
        image_paths = [f"images/enemies/Skeleton/Run/Skeleton_Run_{i}.png" for i in range(1, 13)]
        hurt_image_path = "images/enemies/Skeleton/Hurt/Skeleton_Hurt.png"
        speed = random.randint(self.MIN_SPEED, self.MAX_SPEED)
        hp = random.randint(self.MIN_HP, self.MAX_HP)
        super().__init__(x, y, speed, image_paths, hp, attack_power=3, hurt_image_path=hurt_image_path)

    def update(self, player_x, player_y, player, obstacles):
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

        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.x, self.y = prev_x, prev_y
                self.rect.topleft = (self.x, self.y)
                break

        if self.rect.colliderect(player.rect):
            current_time = time.time()
            if current_time - self.last_attack_time >= 1:
                player.take_damage(self.attack_power)
                self.last_attack_time = current_time

        if self.hurt and time.time() - self.hurt_start_time > 1:  # Восстановление после 1 секунды
            self.hurt = False
