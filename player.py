import pygame
import time

class Player:
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.speed = speed
        self.hp = self.max_hp = 100
        self.attack_power = 10
        self.current_sprite = 0
        self.is_facing_left = False
        self.is_moving = False
        self.hurt = False
        self.hurt_start_time = 0

        self.images_right = self.load_images("images/hero/Punk/Run/Punk_run_{}.png", 6)
        self.images_left = [pygame.transform.flip(image, True, False) for image in self.images_right]
        self.idle_images_right = self.load_images("images/hero/Punk/Idle/Punk_idle_{}.png", 4)
        self.idle_images_left = [pygame.transform.flip(image, True, False) for image in self.idle_images_right]
        self.hurt_image_right = pygame.transform.scale(pygame.image.load("images/hero/Punk/Hurt/Punk_hurt.png"), (75, 75))
        self.hurt_image_left = pygame.transform.flip(self.hurt_image_right, True, False)

        self.rect = pygame.Rect(self.x, self.y, 75, 75)

    def load_images(self, pattern, count):
        return [pygame.transform.scale(pygame.image.load(pattern.format(i)), (75, 75)) for i in range(1, count + 1)]

    def update(self, keys, map_width, map_height, obstacles):
        self.is_moving = False
        prev_x, prev_y = self.x, self.y

        if keys[pygame.K_w]: self.move(0, -self.speed)
        if keys[pygame.K_s]: self.move(0, self.speed)
        if keys[pygame.K_a]: self.move(-self.speed, 0, True)
        if keys[pygame.K_d]: self.move(self.speed, 0, False)

        self.rect.topleft = (self.x, self.y)
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.x, self.y = prev_x, prev_y
                self.rect.topleft = (self.x, self.y)
                break

        self.clamp_position(map_width, map_height)
        
        if self.hurt and time.time() - self.hurt_start_time > 1:  # Recovery after 1 second
            self.hurt = False

    def move(self, dx, dy, facing_left=None):
        self.x += dx
        self.y += dy
        self.is_moving = True
        if facing_left is not None:
            self.is_facing_left = facing_left

    def draw(self, screen, camera_x, camera_y):
        if self.hurt:
            image = self.hurt_image_left if self.is_facing_left else self.hurt_image_right
        else:
            if self.is_moving:
                images = self.images_left if self.is_facing_left else self.images_right
                self.current_sprite = (self.current_sprite + 0.1) % len(images)
            else:
                images = self.idle_images_left if self.is_facing_left else self.idle_images_right
                self.current_sprite = 0  # Reset animation when stopped
            image = images[int(self.current_sprite)]
        
        screen.blit(image, (self.x - camera_x, self.y - camera_y))
        self.draw_health_bar(screen, camera_x, camera_y)

    def clamp_position(self, map_width, map_height):
        self.x = max(0, min(self.x, map_width - 75))
        self.y = max(0, min(self.y, map_height - 75))

    def draw_health_bar(self, screen, camera_x, camera_y):
        bar_length = 75
        bar_height = 10
        fill = (self.hp / self.max_hp) * bar_length

        health_bar_x = self.x - camera_x
        health_bar_y = self.y + 80 - camera_y

        outline_rect = pygame.Rect(health_bar_x, health_bar_y, bar_length, bar_height)
        fill_rect = pygame.Rect(health_bar_x, health_bar_y, fill, bar_height)

        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        self.hurt = True
        self.hurt_start_time = time.time()