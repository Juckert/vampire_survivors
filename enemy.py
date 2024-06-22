import pygame
from abc import ABC, abstractmethod
import time
import random

class Enemy(ABC):
    def __init__(self, x, y, speed, image_paths, hp, attack_power):
        self.x, self.y = x, y
        self.speed = speed
        self.hp, self.attack_power = hp, attack_power
        self.images_right = self.load_images(image_paths)
        self.images_left = [pygame.transform.flip(image, True, False) for image in self.images_right]
        self.current_sprite, self.is_facing_left = 0, False
        self.rect = pygame.Rect(self.x, self.y, 75, 75)
        self.last_attack_time = 0

    def load_images(self, paths):
        return [pygame.transform.scale(pygame.image.load(path), (75, 75)) for path in paths]

    @abstractmethod
    def update(self, player_x, player_y, player, obstacles):
        pass

    def draw(self, screen, camera_x, camera_y):
        images = self.images_left if self.is_facing_left else self.images_right
        screen.blit(images[int(self.current_sprite)], (self.x - camera_x, self.y - camera_y))
        self.current_sprite = (self.current_sprite + 0.08) % len(images)

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)

class Knight(Enemy):
    MIN_SPEED = 1
    MAX_SPEED = 5
    MIN_HP = 30
    MAX_HP = 70

    def __init__(self, x, y):
        image_paths = [f"images/enemies/Knight/Run/Knight_Run_{i}.png" for i in range(1, 9)]
        speed = random.randint(self.MIN_SPEED, self.MAX_SPEED)
        hp = random.randint(self.MIN_HP, self.MAX_HP)
        super().__init__(x, y, speed, image_paths, hp, attack_power=5)

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
