"""
UNDERCOOKED! 1 - si mauvais qu'on sait qu'il y en aura un deuxième

Travail pratique 2, Maintenance logicielle (420-5GP-BB), automne 2023, Collège Bois-de-Boulogne.
Ce logiciel comporte plusieurs opportunités de réusinage, de correction et d'amélioration du code.
Il permet aussi l'ajout de fonctionnalités diverses.

Le sujet est inspiré des jeux multijoueurs coopératifs OVERCOOKED! (2016) et OVERCOOKED!2 (2018)
développés par Ghost Town Games et publiés par Team17.
"""
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # cache le message affiché à l'initialisation de Pygame
import pygame

import settings
from game import Game


def __undercooked() -> None:
    """ La source de tous les maux. """

    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption('Undercooked')
    pygame.mouse.set_visible(False)

    game = Game(screen)
    game.run()

    pygame.quit()


if __name__ == '__main__':
    try:
        __undercooked()
    except KeyboardInterrupt:
        pass
