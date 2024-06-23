import pygame

class Fireball:
    def __init__(self, x, y, direction):
        self.image = pygame.transform.scale(pygame.image.load("images/hero/Punk/Weapon/FB001.png"), (50, 50))
        self.x = x
        self.y = y
        self.speed = 10
        self.direction = direction
        self.rect = self.image.get_rect(center=(self.x, self.y))

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

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.x - camera_x, self.y - camera_y))