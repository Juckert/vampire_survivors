import pygame

class Player:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.current_sprite = 0
        self.is_facing_left = False
        self.is_moving = False

        # Загрузка изображений
        self.images_right = self.load_images("images\\hero\\Punk\\idle\\idle_", 4)
        self.images_left = [pygame.transform.flip(image, True, False) for image in self.images_right]
        self.images_run_right = self.load_images("images\\hero\\Punk\\Run\\Run_", 6)
        self.images_run_left = [pygame.transform.flip(image, True, False) for image in self.images_run_right]

        self.rect = pygame.Rect(self.x, self.y, 75, 75)

    def load_images(self, path, count):
        """Загрузка и масштабирование изображений."""
        return [pygame.transform.scale(pygame.image.load(f"{path}{i+1}.png"), (75, 75)) for i in range(count)]

    def update(self, keys, map_width, map_height, obstacles):
        prev_x, prev_y = self.x, self.y
        self.is_moving = False
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.is_facing_left = True
            self.is_moving = True
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.is_facing_left = False
            self.is_moving = True
        if keys[pygame.K_UP]:
            self.y -= self.speed
            self.is_moving = True
        elif keys[pygame.K_DOWN]:
            self.y += self.speed
            self.is_moving = True

        self.rect.topleft = (self.x, self.y)
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.x, self.y = prev_x, prev_y
                self.rect.topleft = (self.x, self.y)
                break

        self.update_sprite()
        self.clamp_position(map_width, map_height)

    def update_sprite(self):
        """Обновление текущего спрайта в зависимости от состояния."""
        if self.is_moving:
            if self.is_facing_left:
                self.current_sprite = (self.current_sprite + 0.08) % len(self.images_run_left)
            else:
                self.current_sprite = (self.current_sprite + 0.08) % len(self.images_run_right)
        else:
            if self.is_facing_left:
                self.current_sprite = (self.current_sprite + 0.08) % len(self.images_left)
            else:
                self.current_sprite = (self.current_sprite + 0.08) % len(self.images_right)

    def clamp_position(self, map_width, map_height):
        """Ограничение позиции персонажа по границам карты."""
        self.x = max(0, min(self.x, map_width - 75))
        self.y = max(0, min(self.y, map_height - 75))

    def draw(self, screen, camera_x, camera_y):
        if self.is_moving:
            if self.is_facing_left:
                screen.blit(self.images_run_left[int(self.current_sprite)], (self.x - camera_x, self.y - camera_y))
            else:
                screen.blit(self.images_run_right[int(self.current_sprite)], (self.x - camera_x, self.y - camera_y))
        else:
            if self.is_facing_left:
                screen.blit(self.images_left[int(self.current_sprite)], (self.x - camera_x, self.y - camera_y))
            else:
                screen.blit(self.images_right[int(self.current_sprite)], (self.x - camera_x, self.y - camera_y))
