import pygame

class Player:
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.speed = speed
        self.hp = self.max_hp = 100
        self.attack_power = 10
        self.current_sprite = 0
        self.is_facing_left = False
        self.is_moving = False

        self.images_right = self.load_images("images/hero/Punk/Run/Punk_run_{}.png", 6)
        self.images_left = [pygame.transform.flip(image, True, False) for image in self.images_right]

        self.idle_images_right = self.load_images("images/hero/Punk/Idle/Punk_idle_{}.png", 4)
        self.idle_images_left = [pygame.transform.flip(image, True, False) for image in self.idle_images_right]

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

    def move(self, dx, dy, facing_left=None):
        self.x += dx
        self.y += dy
        self.is_moving = True
        if facing_left is not None:
            self.is_facing_left = facing_left

    def draw(self, screen, camera_x, camera_y):
        if self.is_moving:
            images = self.images_left if self.is_facing_left else self.images_right
            self.current_sprite = (self.current_sprite + 0.1) % len(images)
        else:
            images = self.idle_images_left if self.is_facing_left else self.idle_images_right
            self.current_sprite = 0  # Сбрасываем анимацию при остановке

        screen.blit(images[int(self.current_sprite)], (self.x - camera_x, self.y - camera_y))

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
