import pygame
from abc import ABC

class Obstacle(ABC):
    def __init__(self, x, y, image_path):
        self._x = x
        self._y = y
        self._image = pygame.transform.scale(pygame.image.load(image_path), (75, 75))
        self._rect = self._image.get_rect(topleft=(self._x, self._y))

    @property
    def rect(self):
        return self._rect

    def draw(self, screen, camera_x, camera_y):
        ''' Отрисовка изображения препятствия '''
        screen.blit(self._image, (self._x - camera_x, self._y - camera_y))

class Rock(Obstacle):
    ''' Создание класса Rock'''
    def __init__(self, x, y):
        super().__init__(x, y, "images/let/Rocks/Rock_1.png")

class Tree(Obstacle):
    ''' Создание класса Tree'''
    _TREE_IMAGES = {
        "birch": "images/let/Tree/Birch/Birch_xl.png",
        "oak": "images/let/Tree/oak/oak_xl.png",
        "withered_tree": "images/let/Tree/Withered_tree/Withered_tree_xl.png",
        "withered_white_tree": "images/let/Tree/Withered_white_tree/Withered_white_tree_xl.png",
    }

    def __init__(self, x, y, tree_type):
        image_path = self._TREE_IMAGES.get(tree_type)
        if not image_path:
            raise ValueError(f"Invalid tree type: {tree_type}")
        super().__init__(x, y, image_path)