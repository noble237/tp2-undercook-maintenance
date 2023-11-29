import random
import typing
from enum import Enum, auto

import pygame

from food import Food
import settings


class BeverageType(Enum):
    """
    Les différents types de boisson présents dans le jeu.
    """
    COLA = auto(),
    ORANGE_SODA = auto(),
    LEMON_SODA = auto(),
    LEMONADE = auto(),
    PINK_LEMONADE = auto()


class Beverage(Food):
    """
    Boisson qu'on retrouve avec certains repas.
    """

    __BEVERAGES = {BeverageType.COLA: settings.COLA_COLOR,
                   BeverageType.ORANGE_SODA: settings.ORANGE_SODA_COLOR,
                   BeverageType.LEMON_SODA: settings.LEMON_SODA_COLOR,
                   BeverageType.LEMONADE: settings.LEMONADE_COLOR,
                   BeverageType.PINK_LEMONADE: settings.PINK_LEMONADE_COLOR}

    def __init__(self, beverage_type: BeverageType) -> None:
        """
        Initialise la boisson.
        :param beverage_type: type de boisson
        """
        super().__init__()
        self.__type = beverage_type

        self.__width = 24
        self.__height = 40

        self.__color = Beverage.__BEVERAGES[self.__type]

    def draw(self, surface: pygame.Surface, pos: tuple) -> None:
        """
        Dessine la boisson sur une surface à la position spécifiée.
        :param surface: surface sur laquelle dessiner
        :param pos: position dans la surface où dessiner la boisson
        :return: aucun
        """
        rect = pygame.Rect((pos[0] + 2, pos[1]), (20, 40))
        pygame.draw.rect(surface, settings.CUP_COLOR, rect)
        rect = pygame.Rect((pos[0] + 1, pos[1]), (22, 30))
        pygame.draw.rect(surface, settings.CUP_COLOR, rect)
        rect = pygame.Rect((pos[0], pos[1]), (24, 20))
        pygame.draw.rect(surface, settings.CUP_COLOR, rect)

        pygame.draw.circle(surface, self.__color, (pos[0] + 12, pos[1] + 12), 7)

    def color(self) -> tuple:
        return self.__color

    def height(self) -> int:
        return self.__height

    def width(self) -> int:
        return self.__width

    @classmethod
    def random(cls) -> typing.Self or None:
        """
        Crée (ou pas) une boisson aléatoirement. La création s'effectue selon une probabilité
        de présence d'une boisson dans une commande.
        :return: une boisson ou None (pas de boisson)
        """
        if random.randint(0, 100) <= settings.PROBABILITY_FOR_BEVERAGE:
            return cls(random.choice([member for member in BeverageType]))

        return None
