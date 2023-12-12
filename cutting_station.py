import threading
import time

import pygame

from ingredients import Ingredient, IngredientType
import settings

class CuttingStation(pygame.sprite.Sprite):
    """
    Station de découpage pour les ingrédients.
    """

    WIDTH = 60
    HEIGHT = 60

    __STATE_EMPTY = 0
    __STATE_CUTTING = 1
    __STATE_READY = 2

    __CUTTING_TIME = 1.50  # Temps de découpe en secondes

    def __init__(self, pos: tuple) -> None:
        """
        Initialise la station de découpage.
        :param pos: position de la station à l'écran
        """
        super().__init__()

        self.__ingredient = None
        self.__state = CuttingStation.__STATE_EMPTY

        self.image = self.__build_surface()

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def reset(self):
        """
        Réinitialise la station de découpe à son état initial.
        """

        self.__ingredient = None
        self.__state = CuttingStation.__STATE_EMPTY
        self.image = self.__build_surface()


    def start_cutting(self, ingredient: Ingredient) -> None:
        """
        Commence la découpe de l'ingrédient.
        :param ingredient: ingrédient à découper
        :return: aucun
        """
        if self.__state == CuttingStation.__STATE_EMPTY and ingredient.is_for_cutting():
            self.__ingredient = ingredient
            self.__state = CuttingStation.__STATE_CUTTING
            self.image = self.__build_surface()
            cutting_thread = threading.Thread(target=self.__cut)
            cutting_thread.start()     

    def get_cut_ingredient(self) -> Ingredient or None:
        """
        Récupère l'ingrédient découpé si disponible.
        :return: ingrédient découpé ou None
        """
        if self.__state == CuttingStation.__STATE_READY:
            self.__state = CuttingStation.__STATE_EMPTY
            cut_ingredient, self.__ingredient = self.__ingredient, None

            self.image = self.__build_surface()
            return cut_ingredient

        return None


    def is_available(self) -> bool:
        """
        Vérifie si la station est disponible pour une nouvelle découpe.
        :return: True si disponible, False sinon
        """
        return self.__state == CuttingStation.__STATE_EMPTY
    

    def is_ready(self) -> bool:
        """
        Vérifie si la station a fini le découpage.
        :return: True si oui, False sinon
        """
        return self.__state == CuttingStation.__STATE_READY
    

    def __build_surface(self) -> pygame.Surface:
        """
        Construit l'image représentant la station de découpage avec un motif.
        :return: image de la station
        """
        surface = pygame.Surface((60, 60), flags=pygame.SRCALPHA)

        for y in range(0, 60, 12):
            for x in range(0, 60, 12):
                rect = pygame.Rect(x, y, 12, 12)
                if (x // 12) % 2 == (y // 12) % 2:
                    pygame.draw.rect(surface, settings.CUTTING_STATION_COLOR, rect)
                else:
                    pygame.draw.rect(surface, settings.CUTTING_STATION_DARK_COLOR, rect)

        if self.__ingredient:
            x = (60 - self.__ingredient.width()) / 2
            y = (60 - self.__ingredient.height()) / 2
            self.__ingredient.draw(surface, (x, y))

        return surface


    def __cut(self) -> None:
        """ 
        Procède à la découpe de l'ingrédient.
        :return: aucun
        """
        time.sleep(CuttingStation.__CUTTING_TIME)
        self.__state = CuttingStation.__STATE_READY
        self.__ingredient = self.__transform_ingredient(self.__ingredient)
        self.image = self.__build_surface()


    
    def __transform_ingredient(self, ingredient: Ingredient) -> Ingredient:
        """
        Transforme l'ingrédient en sa version découpée.
        :param ingredient: ingrédient à transformer
        :return: ingrédient transformé
        """
        transformed_ingredients_types = {
            IngredientType.UNPREPARED_ONION: IngredientType.ONION_SLICES,
            IngredientType.UNPREPARED_LETTUCE: IngredientType.LETTUCE_SLICES,
            IngredientType.UNPREPARED_TOMATO: IngredientType.TOMATO_SLICES,
            IngredientType.UNPREPARED_PICKLE: IngredientType.PICKLE_SLICE,
            IngredientType.POTATO: IngredientType.POTATO_SLICES
        }

        if ingredient.ingredient_type() in transformed_ingredients_types:
            return Ingredient(transformed_ingredients_types[ingredient.ingredient_type()])
        
        return None
    