import random
import typing

import pygame

import settings
from food import Food


class Fries(Food):
    """
    Cornet de frites.
    """

    def __init__(self) -> None:
        """
        Initialise le cornet de frites.
        """
        super().__init__()

        self.__width = 26
        self.__height = 36

    def draw(self, surface: pygame.Surface, pos: tuple) -> None:
        """
        Dessine le cornet de frites sur la surface spécifiée à la position donnée.
        :param surface: surface sur laquelle dessiner le cornet de frites
        :param pos: position où dessiner le cornet de frites
        :return: aucun
        """
        x, y = pos

        rect = pygame.Rect((x + 2, y + 10), (22, 26))
        pygame.draw.rect(surface, settings.HOLDER_COLOR, rect)
        rect = pygame.Rect((x + 1, y + 10), (24, 18))
        pygame.draw.rect(surface, settings.HOLDER_COLOR, rect)
        rect = pygame.Rect((x, y + 10), (26, 10))
        pygame.draw.rect(surface, settings.HOLDER_COLOR, rect)

        rect = pygame.Rect((x + 6, y + 2), (14, 14))
        pygame.draw.rect(surface, settings.FRIES_COLOR, rect)
        rect = pygame.Rect((x + 2, y + 4), (22, 10))
        pygame.draw.rect(surface, settings.FRIES_COLOR, rect)
        rect = pygame.Rect((x + 14, y), (4, 2))
        pygame.draw.rect(surface, settings.FRIES_COLOR, rect)

    def height(self) -> int:
        return self.__height

    def width(self) -> int:
        return self.__width

    @classmethod
    def random(cls) -> typing.Self or None:
        """
        Crée (ou pas) un cornet de frites aléatoirement. La création s'effectue selon une probabilité
        de présence d'un cornet de frites dans une commande.
        :return: un cornet de frites ou None (pas de frites)
        """
        if random.randint(0, 100) <= settings.PROBABILITY_FOR_FRIES:
            return cls()

        return None
