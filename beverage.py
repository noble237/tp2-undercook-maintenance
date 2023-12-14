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
        if self.buffer_surface is None:
            self.buffer_surface = pygame.Surface((self.width(), self.height()), pygame.SRCALPHA)
            self.buffer_surface.fill((0, 0, 0, 0))

            # Dessin de la boisson sur la surface tampon
            
            rect = pygame.Rect((2, 0), (20, 40))
            pygame.draw.rect(self.buffer_surface, settings.CUP_COLOR, rect)
            rect = pygame.Rect((1, 0), (22, 30))
            pygame.draw.rect(self.buffer_surface, settings.CUP_COLOR, rect)
            rect = pygame.Rect((0, 0), (24, 20))
            pygame.draw.rect(self.buffer_surface, settings.CUP_COLOR, rect)
            pygame.draw.circle(self.buffer_surface, self.__color, (12, 12), 7)

        surface.blit(self.buffer_surface, pos)

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
