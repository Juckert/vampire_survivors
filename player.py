import pygame
from abc import ABC, abstractmethod
import time
import random
from fireball import Fireball

class Player(ABC):
    BASE_SPEED = 50
    BASE_HP = 100
    BASE_ATTACK_POWER = 10

    def __init__(self, x, y, speed_coeff, hp_coeff, attack_power_coeff):
        self._x = x
        self._y = y
        self._speed = int(self.BASE_SPEED * speed_coeff)
        self._hp = int(self.BASE_HP * hp_coeff)
        self._attack_power = int(self.BASE_ATTACK_POWER * attack_power_coeff)
        self._current_sprite = 0
        self._is_facing_left = False
        self._is_moving = False
        self._hurt = False
        self._hurt_start_time = 0

        self._images_right = []
        self._images_left = []
        self._idle_images_right = []
        self._idle_images_left = []
        self._hurt_image_right = None
        self._hurt_image_left = None
        self._hurt_image_2_right = None
        self._hurt_image_2_left = None

        self._rect = pygame.Rect(self._x, self._y, 75, 75)
        self._fireballs = []
        self._last_fire_time = 0
        self._fire_delay = 0.5

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def speed(self):
        return self._speed

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value

    @property
    def attack_power(self):
        return self._attack_power

    @abstractmethod
    def update(self, keys, map_width, map_height, obstacles):
        pass

    def move(self, dx, dy, facing_left=None):
        self._x += dx
        self._y += dy
        self._is_moving = True
        if facing_left is not None:
            self._is_facing_left = facing_left

    def draw(self, screen, camera_x, camera_y):
        self._draw_player(screen, camera_x, camera_y)
        self._draw_fireballs(screen, camera_x, camera_y)

    def _draw_player(self, screen, camera_x, camera_y):
        if self._hurt:
            if self._is_moving:
                image = self._hurt_image_2_left if self._is_facing_left else self._hurt_image_2_right
            else:
                image = self._hurt_image_left if self._is_facing_left else self._hurt_image_right
        else:
            if self._is_moving:
                images = self._images_left if self._is_facing_left else self._images_right
                self._current_sprite = (self._current_sprite + 0.1) % len(images)
            else:
                images = self._idle_images_left if self._is_facing_left else self._idle_images_right
                self._current_sprite = 0
            image = images[int(self._current_sprite)]

        screen.blit(image, (self._x - camera_x, self._y - camera_y))
        self._draw_health_bar(screen, camera_x, camera_y)

    def _draw_health_bar(self, screen, camera_x, camera_y):
        bar_length = 75
        bar_height = 10
        fill = min((self._hp / self.BASE_HP) * bar_length, bar_length)

        health_bar_x = self._x - camera_x
        health_bar_y = self._y + 80 - camera_y

        outline_rect = pygame.Rect(health_bar_x, health_bar_y, bar_length, bar_height)
        fill_rect = pygame.Rect(health_bar_x, health_bar_y, fill, bar_height)

        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)

    def take_damage(self, damage):
        self._hp = max(0, self._hp - damage)
        self._hurt = True
        self._hurt_start_time = time.time()

    def attack_enemy(self, enemy):
        enemy.take_damage(self._attack_power)

    def clamp_position(self, map_width, map_height):
        self._x = max(0, min(self._x, map_width - 75))
        self._y = max(0, min(self._y, map_height - 75))

    def _draw_fireballs(self, screen, camera_x, camera_y):
        for fireball in self._fireballs:
            fireball.draw(screen, camera_x, camera_y)

    def _update_fireballs(self, map_width, map_height, obstacles):
        for fireball in self._fireballs[:]:
            fireball.update()
            if (fireball._x < 0 or fireball._x > map_width or
                fireball._y < 0 or fireball._y > map_height):
                self._fireballs.remove(fireball)
            else:
                for obstacle in obstacles:
                    if fireball.rect.colliderect(obstacle.rect):
                        self._fireballs.remove(fireball)
                        break

    def _load_images(self, paths):
        return [pygame.transform.scale(pygame.image.load(path), (75, 75)) for path in paths]

class Punk(Player):
    def __init__(self, x, y):
        speed_coeff = 1.2
        hp_coeff = 1.3
        attack_power_coeff = 1.1
        super().__init__(x, y, speed_coeff, hp_coeff, attack_power_coeff)
        self._images_right = self._load_images([
            "images/hero/Punk/Run/Punk_run_1.png",
            "images/hero/Punk/Run/Punk_run_2.png",
            "images/hero/Punk/Run/Punk_run_3.png",
            "images/hero/Punk/Run/Punk_run_4.png",
            "images/hero/Punk/Run/Punk_run_5.png",
            "images/hero/Punk/Run/Punk_run_6.png"
        ])
        self._images_left = [pygame.transform.flip(image, True, False) for image in self._images_right]
        self._idle_images_right = self._load_images([
            "images/hero/Punk/Idle/Punk_idle_1.png",
            "images/hero/Punk/Idle/Punk_idle_2.png",
            "images/hero/Punk/Idle/Punk_idle_3.png",
            "images/hero/Punk/Idle/Punk_idle_4.png"
        ])
        self._idle_images_left = [pygame.transform.flip(image, True, False) for image in self._idle_images_right]
        self._hurt_image_right = pygame.transform.scale(pygame.image.load("images/hero/Punk/Hurt/Punk_hurt.png"), (75, 75))
        self._hurt_image_left = pygame.transform.flip(self._hurt_image_right, True, False)
        self._hurt_image_2_right = pygame.transform.scale(pygame.image.load("images/hero/Punk/Hurt/Punk_hurt_2.png"), (75, 75))
        self._hurt_image_2_left = pygame.transform.flip(self._hurt_image_2_right, True, False)

    def update(self, keys, map_width, map_height, obstacles):
        self._is_moving = False
        prev_x, prev_y = self._x, self._y

        if keys[pygame.K_w]: self.move(0, -self.speed)
        if keys[pygame.K_s]: self.move(0, self.speed)
        if keys[pygame.K_a]: self.move(-self.speed, 0, True)
        if keys[pygame.K_d]: self.move(self.speed, 0, False)

        if keys[pygame.K_SPACE]:
            self.shoot_fireball()

        self._rect.topleft = (self._x, self._y)
        for obstacle in obstacles:
            if self._rect.colliderect(obstacle.rect):
                self._x, self._y = prev_x, prev_y
                self._rect.topleft = (self._x, self._y)
                break

        self.clamp_position(map_width, map_height)

        if self._hurt and time.time() - self._hurt_start_time > 1:
            self._hurt = False

        self._update_fireballs(map_width, map_height, obstacles)

    def shoot_fireball(self):
        current_time = time.time()
        if current_time - self._last_fire_time >= self._fire_delay:
            direction = "left" if self._is_facing_left else "right"
            fireball = Fireball(self._x, self._y, direction, "Punk")
            self._fireballs.append(fireball)
            self._last_fire_time = current_time

class Cyborg(Player):
    def __init__(self, x, y):
        speed_coeff = 1.1
        hp_coeff = 1.3
        attack_power_coeff = 1.5
        super().__init__(x, y, speed_coeff, hp_coeff, attack_power_coeff)
        self._images_right = self._load_images([
            "images/hero/Cyborg/Run/Cyborg_run_1.png",
            "images/hero/Cyborg/Run/Cyborg_run_2.png",
            "images/hero/Cyborg/Run/Cyborg_run_3.png",
            "images/hero/Cyborg/Run/Cyborg_run_4.png",
            "images/hero/Cyborg/Run/Cyborg_run_5.png",
            "images/hero/Cyborg/Run/Cyborg_run_6.png"
        ])
        self._images_left = [pygame.transform.flip(image, True, False) for image in self._images_right]
        self._idle_images_right = self._load_images([
            "images/hero/Cyborg/Idle/Cyborg_idle_1.png",
            "images/hero/Cyborg/Idle/Cyborg_idle_2.png",
            "images/hero/Cyborg/Idle/Cyborg_idle_3.png",
            "images/hero/Cyborg/Idle/Cyborg_idle_4.png"
        ])
        self._idle_images_left = [pygame.transform.flip(image, True, False) for image in self._idle_images_right]
        self._hurt_image_right = pygame.transform.scale(pygame.image.load("images/hero/Cyborg/Hurt/Cyborg_hurt_1.png"), (75, 75))
        self._hurt_image_left = pygame.transform.flip(self._hurt_image_right, True, False)
        self._hurt_image_2_right = pygame.transform.scale(pygame.image.load("images/hero/Cyborg/Hurt/Cyborg_hurt_2.png"), (75, 75))
        self._hurt_image_2_left = pygame.transform.flip(self._hurt_image_2_right, True, False)

    def update(self, keys, map_width, map_height, obstacles):
        self._is_moving = False
        prev_x, prev_y = self._x, self._y

        if keys[pygame.K_w]: self.move(0, -self.speed)
        if keys[pygame.K_s]: self.move(0, self.speed)
        if keys[pygame.K_a]: self.move(-self.speed, 0, True)
        if keys[pygame.K_d]: self.move(self.speed, 0, False)

        if keys[pygame.K_SPACE]:
            self.shoot_fireball()

        self._rect.topleft = (self._x, self._y)
        for obstacle in obstacles:
            if self._rect.colliderect(obstacle.rect):
                self._x, self._y = prev_x, prev_y
                self._rect.topleft = (self._x, self._y)
                break

        self.clamp_position(map_width, map_height)

        if self._hurt and time.time() - self._hurt_start_time > 1:
            self._hurt = False

        self._update_fireballs(map_width, map_height, obstacles)

    def shoot_fireball(self):
        current_time = time.time()
        if current_time - self._last_fire_time >= self._fire_delay:
            direction = "left" if self._is_facing_left else "right"
            fireball = Fireball(self._x, self._y, direction, "Cyborg")
            self._fireballs.append(fireball)
            self._last_fire_time = current_time