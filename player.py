import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Загрузка изображения персонажа
        self.image = pygame.image.load("images/player.png")
        self.rect = self.image.get_rect()

        # Начальная позиция персонажа
        self.rect.centerx = 300
        self.rect.bottom = 550

        # Скорость перемещения персонажа
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        # Обновление позиции персонажа
        self.rect.x += self.speed_x

        # Ограничение движения персонажа в пределах экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        

    def move_left(self):
        self.speed_x = -5

    def move_right(self):
        self.speed_x = 5

    def stop(self):
        self.speed_x = 0
        self.speed_y = 0
