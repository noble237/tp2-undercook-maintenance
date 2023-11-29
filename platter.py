import pygame

import settings
from beverage import Beverage
from burger import Burger
from food import Food
from fries import Fries
from meal import Meal


class Platter(pygame.sprite.Sprite):
    """
    Assiette de service. On y place la nourriture pour confectionner un repas avant de l'emballer et de le livrer.
    """

    WIDTH = 60
    HEIGHT = 60

    def __init__(self, pos: tuple) -> None:
        """
        Initialise l'assiette de service.
        :param pos: position où placer l'assiette à l'écran
        """
        super().__init__()

        self.__burger = None
        self.__beverage = None
        self.__fries = None

        self.image = self.__build_surface()

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def add_food(self, food: Food) -> bool:
        """
        Ajoute de la nourriture à l'assiette de service pour confectionner un repas.
        :param food: nourriture à ajouter
        :return: True si l'ajout a fonctionné, False sinon
        """
        if isinstance(food, Burger) and not self.__burger:
            self.__burger = food
            self.image = self.__build_surface()
            return True

        if isinstance(food, Beverage) and not self.__beverage:
            self.__beverage = food
            self.image = self.__build_surface()
            return True

        if isinstance(food, Fries) and not self.__fries:
            self.__fries = food
            self.image = self.__build_surface()
            return True

        return False

    def get_meal(self) -> Meal or None:
        """
        Récupère le repas confectionné sur l'assiette. Un repas doit contenir au minimum un hambourgeois.
        L'assiette de service redevient pleinement disponible si le repas est récupéré.
        :return: le repas si c'est possible, None sinon
        """
        if not self.__burger:
            return None

        meal = Meal()
        meal.add_burger(self.__burger)

        if self.__beverage:
            meal.add_beverage(self.__beverage)

        if self.__fries:
            meal.add_fries(self.__fries)

        self.__burger = self.__beverage = self.__fries = None
        self.image = self.__build_surface()

        return meal

    def __build_surface(self) -> pygame.Surface:
        """
        Construit l'image représentant l'assiette de service et le repas en cours de confection.
        :return: surface représentant l'assiette
        """
        surface = pygame.Surface((Platter.WIDTH, Platter.HEIGHT), flags=pygame.SRCALPHA)

        pygame.draw.circle(surface, settings.PLATTER_COLOR, (30, 30), 30)
        pygame.draw.circle(surface, settings.PLATTER_DARK_COLOR, (30, 30), 26)

        if self.__beverage:
            x = (surface.get_width() - 32) / 2 - 8
            y = surface.get_height() - 54
            self.__beverage.draw(surface, (x, y))

        if self.__fries:
            x = (surface.get_width() - 32) / 2 + 14
            y = surface.get_height() - 46
            self.__fries.draw(surface, (x, y))

        if self.__burger:
            x = (surface.get_width() - self.__burger.width()) / 2
            y = surface.get_height() - 4 - self.__burger.height()
            self.__burger.draw(surface, (x, y))

        return surface
