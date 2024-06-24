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
        self._x = x
        self._y = y
        self._speed = random.randint(int(self.BASE_MIN_SPEED * speed_coeff), int(self.BASE_MAX_SPEED * speed_coeff))
        self._hp = random.randint(int(self.BASE_MIN_HP * hp_coeff), int(self.BASE_MAX_HP * hp_coeff))
        self._attack_power = int(self.BASE_ATTACK_POWER * attack_power_coeff)
        self._images_right = self._load_images(image_paths)
        self._images_left = [pygame.transform.flip(image, True, False) for image in self._images_right]
        self._current_sprite = 0
        self._is_facing_left = False
        self._rect = pygame.Rect(self._x, self._y, 75, 75)
        self._last_attack_time = 0
        self._hurt = False
        self._hurt_start_time = 0
        self._hurt_image_right = None
        self._hurt_image_left = None
        if hurt_image_path:
            self._hurt_image_right = pygame.transform.scale(pygame.image.load(hurt_image_path), (75, 75))
            self._hurt_image_left = pygame.transform.flip(self._hurt_image_right, True, False)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def speed(self):
        return self._speed

    @property
    def hp(self):
        return self._hp

    @property
    def attack_power(self):
        return self._attack_power

    def _load_images(self, paths):
        return [pygame.transform.scale(pygame.image.load(path), (75, 75)) for path in paths]

    def _update_position(self, player_x, player_y):
        prev_x, prev_y = self._x, self._y

        if abs(self._x - player_x) > abs(self._y - player_y):
            if self._x < player_x:
                self._x += self._speed
                self._is_facing_left = False
            else:
                self._x -= self._speed
                self._is_facing_left = True
        else:
            if self._y < player_y:
                self._y += self._speed
            else:
                self._y -= self._speed

        self._rect.topleft = (self._x, self._y)
        return prev_x, prev_y

    def _handle_collisions(self, obstacles):
        for obstacle in obstacles:
            if self._rect.colliderect(obstacle.rect):
                return True
        return False

    def _attack_player(self, player):
        current_time = time.time()
        if self._rect.colliderect(player.rect) and current_time - self._last_attack_time >= 1:
            player.take_damage(self._attack_power)
            self._last_attack_time = current_time

    def update(self, player_x, player_y, player, obstacles):
        prev_x, prev_y = self._update_position(player_x, player_y)

        if self._handle_collisions(obstacles):
            self._x, self._y = prev_x, prev_y
            self._rect.topleft = (self._x, self._y)

        self._attack_player(player)

        if self._hurt and time.time() - self._hurt_start_time > 1:
            self._hurt = False

    def draw(self, screen, camera_x, camera_y):
        if self._hurt:
            image = self._hurt_image_left if self._is_facing_left else self._hurt_image_right
        else:
            images = self._images_left if self._is_facing_left else self._images_right
            image = images[int(self._current_sprite)]
            self._current_sprite = (self._current_sprite + 0.08) % len(images)
        screen.blit(image, (self._x - camera_x, self._y - camera_y))

    def take_damage(self, damage):
        self._hp = max(0, self._hp - damage)
        self._hurt = True
        self._hurt_start_time = time.time()

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
        image_paths = [f"images/enemies/Demon/Run/Demon_Run_{i}.png" for i in range(1, 9)]
        hurt_image_path = "images/enemies/Demon/Hurt/Demon_Hurt.png"
        super().__init__(x, y, speed_coeff, hp_coeff, attack_power_coeff, image_paths, hurt_image_path)