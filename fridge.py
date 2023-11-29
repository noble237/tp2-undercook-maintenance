import pygame

from food import Food
from ingredients import Ingredient
import settings


class Fridge(pygame.sprite.Sprite):
    """
    Réfrigérateur. Chaque réfrigérateur contient une quantité illimitée d'un ingrédient donné.
    """

    def __init__(self, ingredient: Ingredient, pos: tuple) -> None:
        """
        Initialise le réfrigérateur.
        :param ingredient: contenu du réfrigérateur (un seul ingrédient par réfrigérateur)
        :param pos: position du réfrigérateur à l'écran
        """
        super().__init__()

        self.__ingredient = ingredient

        self.image = self.__build_surface()

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def get_food(self) -> Food:
        """
        Récupère un ingrédient du réfrigérateur sous forme de nourriture.
        :return: un des ingrédients réfrigérés
        """
        return self.__ingredient

    def __build_surface(self) -> pygame.Surface:
        """
        Construit l'image représentant le réfrigérateur en fonction de l'ingrédient qu'il contient.
        :return: image du réfrigérateur
        """
        surface = pygame.Surface((50, 40), flags=pygame.SRCALPHA)
        surface.fill(settings.FRIDGE_COLOR)

        self.__ingredient.draw(surface, (9, 10))

        return surface
