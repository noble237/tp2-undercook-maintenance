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


    ########################################## C4 ##########################################
    
    def __build_surface(self) -> pygame.Surface:
        """
        Construit l'image représentant le réfrigérateur en fonction de l'ingrédient qu'il contient.
        :return: image du réfrigérateur
        """

        suface_width = 50
        suface_height = 40

        surface = pygame.Surface((suface_width, suface_height), flags=pygame.SRCALPHA)
        surface.fill(settings.FRIDGE_COLOR)

        # Calculer la position centrée pour l'ingrédient
        ingredient_width = self.__ingredient.width()
        ingredient_height = self.__ingredient.height()

        center_x = (suface_width - ingredient_width) / 2
        center_y = (suface_height - ingredient_height) / 2

        # Dessiner l'ingrédient à la position centrée
        self.__ingredient.draw(surface, (center_x, center_y))

        return surface
    

    ########################################## C4 ##########################################