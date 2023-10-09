import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Загрузка изображения врага (замените на путь к вашему изображению)
        self.image = pygame.image.load("images/enemy.png")
        self.rect = self.image.get_rect()

        # Начальная позиция врага (генерируется случайным образом по X)
        self.rect.x = random.randrange(800 - self.rect.width)
        self.rect.y = random.randrange(40, 50)  # Враги появляются за верхней границей экрана

        # Скорость движения врага (горизонтальное и вертикальное)
        self.speed_y = random.randrange(5, 10)   # Случайная вертикальная скорость

    def update(self):
        # Обновление позиции врага
        self.rect.y += self.speed_y

        # Если враг выходит за границы экрана, перезапустить его в начальной позиции
        if self.rect.top > 600 + 10 or self.rect.left < -10 or self.rect.right > 800 + 10:
            self.rect.x = random.randrange(800 - self.rect.width)
            self.rect.y = random.randrange(40, 100)
            self.speed_y = random.randrange(5, 10)
