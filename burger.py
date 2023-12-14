import random
import typing
import pygame

import settings
from food import Food
from ingredients import Ingredient, IngredientType


class Burger(Food):
    """
    Hambourgeois qu'on retrouve dans tous les repas.
    """

    def __init__(self) -> None:
        """
        Initialise le hambourgeois.
        """
        super().__init__()

        self.__ingredients = []
        self.__width = 0
        self.__height = 0

    def __repr__(self) -> str:
        return str([i.ingredient_type() for i in self.__ingredients])

    def add_ingredients(self, ingredients: list) -> None:
        """
        Ajoute plusieurs ingrédients au hambourgeois.
        :param ingredients: liste des ingrédients à ajouter
        :return: aucun
        """
        self.__ingredients.extend(ingredients)
        self.__width, self.__height = self.__compute_width_and_height()

    
    def add_ingredient(self, ingredient: Ingredient) -> None:
        """
        Ajoute un ingrédient au hambourgeois.
        :param ingredient: ingrédient à ajouter
        :return: aucun
        """

        if self.can_add_ingredient(ingredient):
            self.__ingredients.append(ingredient)
            self.__width, self.__height = self.__compute_width_and_height()
            self.buffer_surface = None


    def can_add_ingredient(self, ingredient: Ingredient):
        # Vérification si l'ingrédient est autorisé pour les burgers
        if not ingredient.is_for_burger():
            return False

        # Le premier ingrédient doit être un BOTTOM_BUN et seulement un seul BOTTOM_BUN est autorisé
        if len(self.__ingredients) == 0:
            return ingredient.ingredient_type() == IngredientType.BOTTOM_BUN
        elif ingredient.ingredient_type() == IngredientType.BOTTOM_BUN:
            return False
        
        # Le deuxième ingrédient doit être un COOKED_PATTY
        if len(self.__ingredients) == 1:
            return ingredient.ingredient_type() == IngredientType.COOKED_PATTY

        # Empêcher l'ajout de tout autre ingrédient si un TOP_BUN est déjà présent
        # seulement un seul TOP_BUN est autorisé
        if any(ingr.ingredient_type() == IngredientType.TOP_BUN for ingr in self.__ingredients):
            return False
        elif len(self.__ingredients) == 1 and ingredient.ingredient_type() == IngredientType.TOP_BUN:
            return False

        # Empêcher l'ajout d'un COOKED_PATTY si 3 ingrédients ou plus sont déjà présents
        if len(self.__ingredients) >= 3 and ingredient.ingredient_type() == IngredientType.COOKED_PATTY:
            return False

        # Ajouter CHEESE_SLICE ou autre ingrédient uniquement si le dernier ingrédient est COOKED_PATTY
        if ingredient.ingredient_type() == IngredientType.CHEESE_SLICE:
            return len(self.__ingredients) > 0 and self.__ingredients[-1].ingredient_type() == IngredientType.COOKED_PATTY
        
        return True

    def draw(self, surface: pygame.Surface, pos: tuple) -> None:
        """
        Dessine le hambourgeois sur une surface à la position spécifiée.
        :param surface: surface sur laquelle dessiner
        :param pos: position dans la surface où dessiner le hambourgeois
        :return: aucun
        """

        # Dessin du burger sur la surface tampon

        if self.buffer_surface is None:
            self.buffer_surface = pygame.Surface((self.width(), self.height()), pygame.SRCALPHA)
            self.buffer_surface.fill((0, 0, 0, 0))

            y = self.height()
            last_patty_y = 0

            for ingredient in self.__ingredients:
                if ingredient.ingredient_type() == IngredientType.COOKED_PATTY:
                    y -= ingredient.height()
                    last_patty_y = y

                if ingredient.ingredient_type() == IngredientType.CHEESE_SLICE:
                    # Dessiner le CHEESE_SLICE à la position Y du dernier COOKED_PATTY
                    ingredient.draw(self.buffer_surface, (0, last_patty_y))
                else:
                    if ingredient.ingredient_type() != IngredientType.COOKED_PATTY:
                        y -= ingredient.height()
                    ingredient.draw(self.buffer_surface, (0, y))

        surface.blit(self.buffer_surface, pos)

    def height(self) -> int:
        return self.__height

    def width(self) -> int:
        return self.__width

    def __compute_width_and_height(self) -> tuple:
        """
        Calcule la hauteur et la largeur (en pixels) du hambourgeois en fonction des ingrédients qui le composent.
        :return: largeur et hauteur du hambourgeois
        """
        width = 0
        height = 0

        for ingredient in self.__ingredients:
            width = max(width, ingredient.width())
            height += ingredient.height()

        return width, height

    ########################################## A2 ##########################################

    @classmethod
    def random(cls) -> typing.Self:
        """
        Crée un hambourgeois contenant le pain du bas, le pain du haut et au moins une boulette.
        Une deuxième boulette est ajoutée selon une probabilité de présence d'une deuxième boulette.
        Une sélection d'options (ex.: tranche de fromage, salade, cornichon, etc.) est également faite au hasard.
        :return: un hanbourgeois
        """
        burger = cls()

        burger.add_ingredients([Ingredient(IngredientType.BOTTOM_BUN), Ingredient(IngredientType.COOKED_PATTY)])
        if random.randint(0, 100) <= settings.PROBABILITY_FOR_TWO_PATTIES:
            burger.add_ingredient(Ingredient(IngredientType.COOKED_PATTY))

        if ingredients := Ingredient.random_burger_options():
            # Séparer le fromage des autres ingrédients
            cheese_slices = [ingr for ingr in ingredients if ingr.ingredient_type() == IngredientType.CHEESE_SLICE]
            other_ingredients = [ingr for ingr in ingredients if ingr.ingredient_type() != IngredientType.CHEESE_SLICE]

            # Ajouter d'abord le fromage, si présent
            for cheese in cheese_slices:
                burger.add_ingredient(cheese)

            # Ajouter ensuite les autres ingrédients
            burger.add_ingredients(other_ingredients)


        burger.add_ingredient(Ingredient(IngredientType.TOP_BUN))

        return burger
    
    ########################################## A2 ##########################################
    
    ########################################## C1 ##########################################
    @property
    def ingredients(self) -> list:
        return self.__ingredients

    ########################################## C1 ##########################################