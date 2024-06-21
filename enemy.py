import pygame
from abc import ABC, abstractmethod
import random

class Enemy(ABC):
    def __init__(self, x, y, speed, image_paths):
        self.x = x
        self.y = y
        self.speed = speed
        self.images_right = self.load_images(image_paths)
        self.images_left = [pygame.transform.flip(image, True, False) for image in self.images_right]
        self.current_sprite = 0
        self.is_facing_left = False
        self.is_moving_vertically = False
        self.rect = pygame.Rect(self.x, self.y, 75, 75)

    def load_images(self, paths):
        return [pygame.transform.scale(pygame.image.load(path), (75, 75)) for path in paths]

    @abstractmethod
    def update(self, player_x, player_y, obstacles):
        pass

    def draw(self, screen, camera_x, camera_y):
        if self.is_facing_left and not self.is_moving_vertically:
            screen.blit(self.images_left[int(self.current_sprite)], (self.x - camera_x, self.y - camera_y))
        else:
            screen.blit(self.images_right[int(self.current_sprite)], (self.x - camera_x, self.y - camera_y))
        self.current_sprite = (self.current_sprite + 0.08) % len(self.images_right)

class Knight(Enemy):
    def __init__(self, x, y):
        image_paths = [f"images\\enemies\\Knight\\Run\\Knight_Run_{i}.png" for i in range(1, 9)]
        super().__init__(x, y, 3, image_paths)

    def update(self, player_x, player_y, obstacles):
        prev_x, prev_y = self.x, self.y
        
        self.is_moving_vertically = False
        
        if self.x < player_x:
            self.x += self.speed
            self.is_facing_left = False
        elif self.x > player_x:
            self.x -= self.speed
            self.is_facing_left = True
        
        if self.y < player_y:
            self.y += self.speed
            self.is_moving_vertically = True
        elif self.y > player_y:
            self.y -= self.speed
            self.is_moving_vertically = True
        
        self.rect.topleft = (self.x, self.y)
        
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.x, self.y = prev_x, prev_y
                self.rect.topleft = (self.x, self.y)
                break
