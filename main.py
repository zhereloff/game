import pygame
import random
import pygame.time
from game import Game 
from gameVariables import Variables

var = Variables()
game = Game()

# Инициализация PyGame
pygame.init()

game.initialize(var)

game.gameRules(var)

while var.input_active:
    game.waitForName(var)

while var.running:
    game.mainGame(var)
    
# Завершение PyGame
pygame.quit()