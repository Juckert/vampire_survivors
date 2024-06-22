import pygame
from abc import ABC, abstractmethod
import time

class Enemy(ABC):
    def __init__(self, x, y, speed, image_paths, hp, attack_power):
        self.x = x
        self.y = y
        self.speed = speed
        self.images_right = self.load_images(image_paths)
        self.images_left = [pygame.transform.flip(image, True, False) for image in self.images_right]
        self.current_sprite = 0
        self.is_facing_left = False
        self.rect = pygame.Rect(self.x, self.y, 75, 75)
        self.hp = hp  # Здоровье врага
        self.attack_power = attack_power  # Сила атаки врага
        self.last_attack_time = 0  # Время последней атаки

    def load_images(self, paths):
        return [pygame.transform.scale(pygame.image.load(path), (75, 75)) for path in paths]

    @abstractmethod
    def update(self, player_x, player_y, player, obstacles):
        pass

    def draw(self, screen, camera_x, camera_y):
        if self.is_facing_left:
            screen.blit(self.images_left[int(self.current_sprite)], (self.x - camera_x, self.y - camera_y))
        else:
            screen.blit(self.images_right[int(self.current_sprite)], (self.x - camera_x, self.y - camera_y))
        self.current_sprite = (self.current_sprite + 0.08) % len(self.images_right)

    def take_damage(self, damage):
        """Нанесение урона врагу."""
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            # Здесь можно добавить логику уничтожения врага

class Knight(Enemy):
    def __init__(self, x, y):
        image_paths = [f"images\\enemies\\Knight\\Run\\Knight_Run_{i}.png" for i in range(1, 9)]
        super().__init__(x, y, 3, image_paths, hp=50, attack_power=5)

    def update(self, player_x, player_y, player, obstacles):
        prev_x, prev_y = self.x, self.y
        
        if abs(self.x - player_x) > abs(self.y - player_y):
            # Horizontal movement
            if self.x < player_x:
                self.x += self.speed
                self.is_facing_left = False
            else:
                self.x -= self.speed
                self.is_facing_left = True
        else:
            # Vertical movement
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
        
        # Проверка столкновения с игроком для нанесения урона
        if self.rect.colliderect(player.rect):
            current_time = time.time()
            if current_time - self.last_attack_time >= 1:  # Наносить урон раз в секунду
                player.take_damage(self.attack_power)
                self.last_attack_time = current_time

