import pygame
from abc import ABC, abstractmethod

class Obstacle(ABC):
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(image_path), (75, 75))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.x - camera_x, self.y - camera_y))

class Rock(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, "images\\let\\Rocks\\Rock_1.png")

class Tree(Obstacle):
    def __init__(self, x, y, tree_type):
        tree_images = {
            "birch": "images\\let\\Tree\\Birch\\Birch_xl.png",
            "oak": "images\\let\\Tree\\oak\\oak_xl.png",
            "withered_tree": "images\\let\\Tree\\Withered_tree\\Withered_tree_xl.png",
            "withered_white_tree": "images\\let\\Tree\\Withered_white_tree\\Withered_white_tree_xl.png",
        }
        super().__init__(x, y, tree_images[tree_type])