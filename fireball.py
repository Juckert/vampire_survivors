import pygame

class Fireball:
    SPEED = 10
    MAX_DISTANCE = 500

    def __init__(self, x, y, direction):
        self.start_x = x
        self.x = x
        self.y = y
        self.direction = direction
        self.load_images()
        self.image_index = 0
        self.rect = self.images[self.image_index].get_rect(center=(self.x, self.y))
        self.active = True  # Добавляем атрибут, чтобы отслеживать, активен ли fireball

    def load_images(self):
        self.original_images = [pygame.transform.scale(pygame.image.load(f"images\hero\Punk\Weapon\Fireball_{i}.png"), (40, 40)) for i in range(1, 5)]
        if self.direction == "left":
            self.images = [pygame.transform.flip(image, True, False) for image in self.original_images]
        else:
            self.images = self.original_images

    def update(self):
        if self.direction == "right":
            self.x += self.SPEED
        else:
            self.x -= self.SPEED
        self.rect.topleft = (self.x, self.y)
        self.image_index = (self.image_index + 0.2) % len(self.images)
        
        # Проверка пройденного расстояния
        if abs(self.x - self.start_x) > self.MAX_DISTANCE:
            self.active = False

    def draw(self, screen, camera_x, camera_y):
        if self.active:
            current_image = self.images[int(self.image_index)]
            screen.blit(current_image, (self.x - camera_x, self.y - camera_y))
