import pygame

class Fireball:
    SPEED = 10
    MAX_DISTANCE = 500

    def __init__(self, x, y, direction, character_type):
        self._start_x = x
        self._x = x
        self._y = y
        self._direction = direction
        self.character_type = character_type  # Added character_type attribute
        self._load_images()
        self._image_index = 0
        self._rect = self._images[self._image_index].get_rect(center=(self._x, self._y))
        self._active = True

    def _load_images(self):
        if self.character_type == "Punk":
            base_path = "images/hero/Punk/Weapon/Fireball_"  
        elif self.character_type == "Cyborg":
            base_path = "images/hero/Cyborg/Weapon/Fireball_"  
        else:
            raise ValueError("Unknown character type")
        
        self._original_images = [pygame.transform.scale(pygame.image.load(f"{base_path}{i}.png"), (40, 40)) for i in range(1, 5)]
        if self._direction == "left":
            self._images = [pygame.transform.flip(image, True, False) for image in self._original_images]
        else:
            self._images = self._original_images

    def update(self):
        if self._direction == "right":
            self._x += self.SPEED
        else:
            self._x -= self.SPEED
        self._rect.topleft = (self._x, self._y)
        self._image_index = (self._image_index + 0.2) % len(self._images)
        
        if abs(self._x - self._start_x) > self.MAX_DISTANCE:
            self._active = False

    def draw(self, screen, camera_x, camera_y):
        if self._active:
            current_image = self._images[int(self._image_index)]
            screen.blit(current_image, (self._x - camera_x, self._y - camera_y))

    @property
    def active(self):
        return self._active

    @property
    def rect(self):
        return self._rect