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
    POTATO_SLICES = auto(),
    BURNT_PATTY = auto(),


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
                     IngredientType.BURNT_PATTY: (settings.BURNT_PATTY_COLOR, 32, 6),
                     IngredientType.CHEESE_SLICE: (settings.CHEESE_COLOR, 32, 6),
                     IngredientType.ONION_SLICES: (settings.ONIONS_COLOR, 32, 3),
                     IngredientType.LETTUCE_SLICES: (settings.LETTUCE_COLOR, 32, 3),
                     IngredientType.TOMATO_SLICES: (settings.TOMATO_COLOR, 32, 3),
                     ########################################## C5 ##########################################
                     IngredientType.PICKLE_SLICE: (settings.PICKLE_COLOR, 32, 3), # Changement a 32
                     ########################################## C5 ##########################################
                     IngredientType.POTATO_SLICES: (settings.POTATO_COLOR, 16, 16)}

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
    
    __CUTTING_INGREDIENTS = [IngredientType.POTATO,
                 IngredientType.UNPREPARED_ONION,
                 IngredientType.UNPREPARED_LETTUCE,
                 IngredientType.UNPREPARED_TOMATO,
                 IngredientType.UNPREPARED_PICKLE]

    def __init__(self, ingredient_type: IngredientType) -> None:
        """
        Initialise un ingrédient.
        :param ingredient_type: type d'ingrédient
        """
        super().__init__()
        self.__type = ingredient_type

        self.__color, self.__width, self.__height = Ingredient.__INGREDIENTS[self.__type]

    def draw(self, surface: pygame.Surface, pos: tuple) -> None:
        if self.buffer_surface is None:
            self.buffer_surface = pygame.Surface((self.width(), self.height()), pygame.SRCALPHA)
            self.buffer_surface.fill((0, 0, 0, 0))

            # Dessin de l'ingrédient sur la surface tampon

            match self.__type:
                case IngredientType.POTATO:
                    x = self.__width / 2
                    y = self.__height / 2
                    r = self.__width / 2
                    pygame.draw.circle(self.buffer_surface, self.__color, (x, y), r)

                case IngredientType.RAW_PATTY:
                    rect = pygame.Rect((2, 0), (28, self.__height))
                    pygame.draw.rect(self.buffer_surface, self.__color, rect)
                    rect = pygame.Rect((0, 1), (32, self.__height - 2))
                    pygame.draw.rect(self.buffer_surface, self.__color, rect)

                case IngredientType.BOTTOM_BUN:
                    rect = pygame.Rect((0, 0), (32, self.__height / 2))
                    pygame.draw.rect(self.buffer_surface, self.__color, rect)
                    rect = pygame.Rect((2, self.__height / 2), (28, self.__height / 2))
                    pygame.draw.rect(self.buffer_surface, self.__color, rect)

                case IngredientType.TOP_BUN:
                    rect = pygame.Rect((6, 0), (20, self.__height / 4))
                    pygame.draw.rect(self.buffer_surface, self.__color, rect)
                    rect = pygame.Rect((2, self.__height / 4), (28, self.__height / 4))
                    pygame.draw.rect(self.buffer_surface, self.__color, rect)
                    rect = pygame.Rect((0, self.__height / 2), (32, self.__height / 2))
                    pygame.draw.rect(self.buffer_surface, self.__color, rect)

                case IngredientType.COOKED_PATTY | IngredientType.BURNT_PATTY:
                    rect = pygame.Rect((2, 0), (28, self.__height))
                    pygame.draw.rect(self.buffer_surface, self.__color, rect)
                    rect = pygame.Rect((0, 1), (32, self.__height - 2))
                    pygame.draw.rect(self.buffer_surface, self.__color, rect)

                case IngredientType.PICKLE_SLICE:
                    rect = pygame.Rect((-2, 0), (36, self.__height))
                    pygame.draw.rect(self.buffer_surface, self.__color, rect)

                case IngredientType.CHEESE_SLICE:
                    rect = pygame.Rect((0, 0), (32, 1))
                    pygame.draw.rect(self.buffer_surface, self.__color, rect)
                    rect = pygame.Rect((4, 1), (24, 1))
                    pygame.draw.rect(self.buffer_surface, self.__color, rect)
                    rect = pygame.Rect((8, 2), (16, 1))
                    pygame.draw.rect(self.buffer_surface, self.__color, rect)
                    rect = pygame.Rect((12, 3), (8, 1))
                    pygame.draw.rect(self.buffer_surface, self.__color, rect)

                case IngredientType.POTATO_SLICES:
                    for _ in range(random.randint(5, 10)):
                        x = random.randint(0, 20)
                        y = random.randint(-5, 5)
                        width = 2
                        height = random.randint(5, 20)
                        color_variation = [random.randint(-10, 10) for _ in range(3)]
                        frite_color = [max(0, min(255, settings.POTATO_COLOR[i] + color_variation[i])) for i in range(3)]
                        frite_rect = pygame.Rect((x, y), (width, height))
                        pygame.draw.rect(self.buffer_surface, frite_color, frite_rect)

                case _:
                    rect = pygame.Rect((0, 0), (32, self.__height))
                    pygame.draw.rect(self.buffer_surface, self.__color, rect)

        surface.blit(self.buffer_surface, pos)
        
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
    

    def is_for_cutting(self) -> bool:
        return self.__type in Ingredient.__CUTTING_INGREDIENTS

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
