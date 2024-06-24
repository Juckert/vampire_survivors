import pygame

class Fireball:
    def __init__(self, x, y, direction):
        self.images = [pygame.transform.scale(pygame.image.load(f"images/hero/Punk/Weapon/FB00{i}.png"), (50, 50)) for i in range(1, 6)]
        self.x = x
        self.y = y
        self.speed = 10
        self.direction = direction
        self.rect = self.images[0].get_rect(center=(self.x, self.y))
        self.current_frame = 0  # Index of the current frame
        self.animation_speed = 0.1  # Control the speed of animation
        self.time_since_last_frame = 0

    def update(self):
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        self.rect.center = (self.x, self.y)

        # Update animation frame
        self.time_since_last_frame += self.animation_speed
        if self.time_since_last_frame >= 1:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.time_since_last_frame = 0

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.images[self.current_frame], (self.x - camera_x, self.y - camera_y))
