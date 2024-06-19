import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = [
            pygame.image.load('images\punk\idle_1.png'),
            pygame.image.load('images\punk\idle_2.png'),
            pygame.image.load('images\punk\idle_3.png'),
            pygame.image.load('images\punk\idle_4.png')
        ]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def update(self):
        self.current_sprite += 0.002  # изменено значение
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

# Инициализация Pygame
pygame.init()

# Создание экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Создание спрайта
player = Player(100, 100)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление спрайта
    all_sprites.update()

    # Отрисовка
    screen.fill((0, 0, 0))  # Отрисовка фона
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()