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

    display_info = pygame.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
    pygame.display.set_caption('Undercooked')
    pygame.mouse.set_visible(False)

    title_screen = pygame.image.load('img/undercooked1.png')
    title_settings = pygame.transform.scale(title_screen, (screen_width, screen_height))
    screen.blit(title_settings, (0, 0))
    pygame.display.flip()

    pygame.time.wait(2000)

    game = Game(screen)
    game.run()

    pygame.quit()


if __name__ == '__main__':
    try:
        __undercooked()
    except KeyboardInterrupt:
        pass
