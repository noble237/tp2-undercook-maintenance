import pygame

import settings

from burger import Burger
from ingredients import Ingredient, IngredientType



class AssemblyStation(pygame.sprite.Sprite):
    """
    Station d'assemblage pour les hambourgeois.
    """

    def __init__(self, pos: tuple) -> None:
        """
        Initialise la station d'assemblage.
        :param pos: position de la station d'assemblage à l'écran
        """
        super().__init__()

        self.__burger = None

        self.image = self.__build_surface()

        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - self.rect.width / 2
        self.rect.y = pos[1] - self.rect.height / 2


    ########################################## A1 ##########################################

    def add_ingredient(self, ingredient: Ingredient) -> bool:
        """
        Ajoute un ingrédient au hambourgeois en cours d'assemblage.
        :param ingredient: ingrédient à ajouter
        :return: True si l'ingrédient a été ajouté, False sinon
        """
        if isinstance(ingredient, Ingredient) and ingredient.is_for_burger():
            if not self.__burger:
                self.__burger = Burger()

            if self.__burger.can_add_ingredient(ingredient):
                self.__burger.add_ingredient(ingredient)
                self.image = self.__build_surface()
                return True

        return False

    def get_burger(self) -> Burger or None:
        """
        Retire le hambourgeois de la station d'assemblage si le dernier ingrédient est un TOP_BUN.
        :return: hambourgeois assemblé s'il est complet, None sinon
        """
        if self.__burger and self.__burger.ingredients and self.__burger.ingredients[-1].ingredient_type() == IngredientType.TOP_BUN:
            burger, self.__burger = self.__burger, None
            self.image = self.__build_surface()
            return burger

        return None

    
    ########################################## A1 ##########################################


    def __build_surface(self) -> pygame.Surface:
        """
        Construit l'image représentant la station d'assemblage
        :return: la surface (image) construite
        """
        surface = pygame.Surface((60, 60), flags=pygame.SRCALPHA)
        surface.fill(settings.PAPER_COLOR_1)

        for y in range(5):
            for x in range(5):
                if (y * 5 + x) % 2:
                    rect = pygame.Rect(x * 12, y * 12, 12, 12)
                    pygame.draw.rect(surface, settings.PAPER_COLOR_2, rect)

        if self.__burger:
            x = (60 - self.__burger.width()) / 2
            y = 56 - self.__burger.height()
            self.__burger.draw(surface, (x, y))

        return surface
