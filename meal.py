import pygame

import settings
from beverage import Beverage
from burger import Burger
from fries import Fries
from food import Food


class Meal(Food):
    """
    Repas. Un repas peut comprendre trois nourritures: hambourgeois, boisson et frites.
    """

    def __init__(self) -> None:
        super().__init__()

        self.__burger = None
        self.__beverage = None
        self.__fries = None

        self.__width = 30
        self.__height = 30

    def add_beverage(self, beverage: Beverage) -> None:
        """ Ajoute une boisson au repas. """
        if not self.__beverage:
            self.__beverage = beverage

    def add_burger(self, burger: Burger) -> None:
        """ Ajoute un hambourgeois au repas. """
        if not self.__burger:
            self.__burger = burger

    def add_fries(self, fries: Fries) -> None:
        """ Ajoute un cornet de frites au repas. """
        if not self.__fries:
            self.__fries = fries

    def draw(self, surface: pygame.Surface, pos: tuple) -> None:
        """
        Dessine le repas sur la surface spécifiée à la position donnée.
        :param surface: surface sur laquelle dessiner le repas
        :param pos: position où dessiner le repas sur la surface
        :return: aucun
        """
        x, y = pos

        rect = pygame.Rect(x, y, self.__width, 8)
        pygame.draw.rect(surface, settings.MEAL_COLOR, rect)
        rect = pygame.Rect(x + 1, y + 8, self.__width - 2, self.__height - 16)
        pygame.draw.rect(surface, settings.MEAL_COLOR, rect)
        rect = pygame.Rect(x + 1, y + 12, self.__width - 2, 1)
        pygame.draw.rect(surface, settings.MEAL_DARK_COLOR, rect)
        rect = pygame.Rect(x, y + self.__height - 8, self.__width, 8)
        pygame.draw.rect(surface, settings.MEAL_COLOR, rect)

    def height(self) -> int:
        return self.__height

    def width(self) -> int:
        return self.__width
    
    ########################################## C1 ##########################################
    @property
    def burger(self) -> Burger or None:
        return self.__burger

    @property
    def beverage(self) -> Beverage or None:
        return self.__beverage

    @property
    def fries(self) -> Fries or None:
        return self.__fries
    ########################################## C1 ##########################################