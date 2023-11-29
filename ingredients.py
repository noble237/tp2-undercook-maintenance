from enum import Enum, auto
import random

import pygame

from food import Food
import settings


class IngredientType(Enum):
    """
    Types d'ingrédient (transformé ou pas).
    """
    POTATO = auto(),
    RAW_PATTY = auto(),
    UNPREPARED_ONION = auto(),
    UNPREPARED_LETTUCE = auto(),
    UNPREPARED_TOMATO = auto(),
    UNPREPARED_PICKLE = auto(),
    BOTTOM_BUN = auto(),
    TOP_BUN = auto(),
    COOKED_PATTY = auto(),
    CHEESE_SLICE = auto(),
    ONION_SLICES = auto(),
    LETTUCE_SLICES = auto(),
    TOMATO_SLICES = auto(),
    PICKLE_SLICE = auto(),


class Ingredient(Food):
    """
    Ingrédient (transformé ou pas).
    """
    # couleur, largeur, hauteur de tous les ingrédients
    __INGREDIENTS = {IngredientType.POTATO: (settings.POTATO_COLOR, 16, 16),
                     IngredientType.RAW_PATTY: (settings.RAW_PATTY_COLOR, 32, 6),
                     IngredientType.UNPREPARED_ONION: (settings.ONIONS_COLOR, 32, 6),
                     IngredientType.UNPREPARED_LETTUCE: (settings.LETTUCE_COLOR, 32, 6),
                     IngredientType.UNPREPARED_TOMATO: (settings.TOMATO_COLOR, 32, 6),
                     IngredientType.UNPREPARED_PICKLE: (settings.PICKLE_COLOR, 32, 6),
                     IngredientType.BOTTOM_BUN: (settings.BUN_COLOR, 32, 6),
                     IngredientType.TOP_BUN: (settings.BUN_COLOR, 32, 8),
                     IngredientType.COOKED_PATTY: (settings.COOKED_PATTY_COLOR, 32, 6),
                     IngredientType.CHEESE_SLICE: (settings.CHEESE_COLOR, 32, 1),
                     IngredientType.ONION_SLICES: (settings.ONIONS_COLOR, 32, 3),
                     IngredientType.LETTUCE_SLICES: (settings.LETTUCE_COLOR, 32, 3),
                     IngredientType.TOMATO_SLICES: (settings.TOMATO_COLOR, 32, 3),
                     IngredientType.PICKLE_SLICE: (settings.PICKLE_COLOR, 36, 3)}

    # ingrédients qui sont optionnels dans la composition d'un hambourgeois
    __OPTIONS = [IngredientType.CHEESE_SLICE,
                 IngredientType.ONION_SLICES,
                 IngredientType.LETTUCE_SLICES,
                 IngredientType.TOMATO_SLICES,
                 IngredientType.PICKLE_SLICE]

    # tous les ingrédients qui sont permis dans un hambourgeois
    __BURGER_INGREDIENTS = [IngredientType.TOP_BUN,
                            IngredientType.BOTTOM_BUN,
                            IngredientType.COOKED_PATTY,
                            *__OPTIONS]

    def __init__(self, ingredient_type: IngredientType) -> None:
        """
        Initialise un ingrédient.
        :param ingredient_type: type d'ingrédient
        """
        super().__init__()
        self.__type = ingredient_type

        self.__color, self.__width, self.__height = Ingredient.__INGREDIENTS[self.__type]

    def draw(self, surface: pygame.Surface, pos: tuple) -> None:
        """
        Dessine l'ingrédient sur la surface spécifiée à la position donnée.
        :param surface: surface sur laquelle dessiner l'ingrédient
        :param pos: position où dessiner l'ingrédient sur la surface
        :return: aucun
        """
        match self.__type:
            case IngredientType.POTATO:
                x = pos[0] + round(self.__width / 2.0)
                y = pos[1] + round(self.__height / 2.0)
                r = round(self.__width / 2.0)
                pygame.draw.circle(surface, self.__color, (x, y), r)
            case IngredientType.RAW_PATTY:
                rect = pygame.Rect((pos[0] + 2, pos[1]), (28, self.__height))
                pygame.draw.rect(surface, self.__color, rect)
                rect = pygame.Rect((pos[0], pos[1] + 1), (32, self.__height - 2))
                pygame.draw.rect(surface, self.__color, rect)
            case IngredientType.BOTTOM_BUN:
                rect = pygame.Rect((pos[0], pos[1]), (32, self.__height / 2))
                pygame.draw.rect(surface, self.__color, rect)
                rect = pygame.Rect((pos[0] + 2, pos[1] + self.__height / 2), (28, self.__height / 2))
                pygame.draw.rect(surface, self.__color, rect)
            case IngredientType.TOP_BUN:
                rect = pygame.Rect((pos[0] + 6, pos[1]), (20, self.__height / 4))
                pygame.draw.rect(surface, self.__color, rect)
                rect = pygame.Rect((pos[0] + 2, pos[1] + self.__height / 4), (28, self.__height / 4))
                pygame.draw.rect(surface, self.__color, rect)
                rect = pygame.Rect((pos[0], pos[1] + self.__height / 2), (32, self.__height / 2))
                pygame.draw.rect(surface, self.__color, rect)
            case IngredientType.COOKED_PATTY:
                rect = pygame.Rect((pos[0] + 2, pos[1]), (28, self.__height))
                pygame.draw.rect(surface, self.__color, rect)
                rect = pygame.Rect((pos[0], pos[1] + 1), (32, self.__height - 2))
                pygame.draw.rect(surface, self.__color, rect)
            case IngredientType.CHEESE_SLICE:
                rect = pygame.Rect((pos[0], pos[1]), (32, 1))
                pygame.draw.rect(surface, self.__color, rect)
                rect = pygame.Rect((pos[0] + 4, pos[1] + 1), (24, 1))
                pygame.draw.rect(surface, self.__color, rect)
                rect = pygame.Rect((pos[0] + 8, pos[1] + 2), (16, 1))
                pygame.draw.rect(surface, self.__color, rect)
                rect = pygame.Rect((pos[0] + 12, pos[1] + 3), (8, 1))
                pygame.draw.rect(surface, self.__color, rect)
            case IngredientType.PICKLE_SLICE:
                rect = pygame.Rect((pos[0] - 2, pos[1]), (36, self.__height))
                pygame.draw.rect(surface, self.__color, rect)
            case _:
                rect = pygame.Rect(pos, (32, self.__height))
                pygame.draw.rect(surface, self.__color, rect)

    def height(self) -> int:
        return self.__height

    def ingredient_type(self) -> IngredientType:
        return self.__type

    def is_for_burger(self) -> bool:
        """
        Vérifie si un ingrédient peut être placé dans un hambourgeois. Un ingrédient qui requiert
        une transformation (ex.: une boulette de viande crue) n'est pas permis dans un hambourgeois
        (ex.: la boulette doit d'abord être cuite avant d'être placée dans le hambourgeois).
        :return: True si l'ingrédient est permis, False sinon
        """
        return self.__type in Ingredient.__BURGER_INGREDIENTS

    def width(self) -> int:
        return self.__width

    @staticmethod
    def random_burger_options() -> list:
        """
        Retourne une liste aléatoire d'ingrédients optionnels pour un hambourgeois.
        :return: liste d'ingrédients optionnels
        """
        selection = [Ingredient(member) for member in Ingredient.__OPTIONS]
        return random.sample(selection, k=random.randint(0, len(selection)))
