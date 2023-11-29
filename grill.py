import pygame

import threading
import time

from food import Food
from ingredients import Ingredient, IngredientType
import settings


class Grill(pygame.sprite.Sprite):
    """
    Grill pour cuire les boulettes.
    """

    WIDTH = 50
    HEIGHT = 50

    COOKING_TICK = 0.20  # en secondes
    COOKING_STEPS = 30

    def __init__(self, pos: tuple) -> None:
        """
        Initialise le grill.
        :param pos: position du grill à l'écran
        """
        super().__init__()

        self.__cooking = False

        self.__patty = None
        self.__patty_color = settings.RAW_PATTY_COLOR

        self.image = self.__build_surface()

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def cook(self, ingredient: Ingredient) -> None:
        """
        Débute la cuisson d'une boulette. Si l'ingrédient fourni n'est pas une boulette, rien ne se produit.
        La cuisson prend un certain temps. Elle ne sera pas complétée au retour de l'appel de cette méthode.
        :param ingredient: boulette de viande crue
        :return: aucun
        """
        if self.__cooking:
            return

        if not ingredient or ingredient.ingredient_type() != IngredientType.RAW_PATTY:
            return

        self.cooking = True

        self.__patty = ingredient
        self.__patty_color = settings.RAW_PATTY_COLOR

        cooking_thread = threading.Thread(target=self.__cook)
        cooking_thread.start()

    def __cooking_done(self) -> None:
        """
        Finalise la cuisson d'une boulette.
        :return: aucun
        """
        self.patty_color = settings.COOKED_PATTY_COLOR
        self.__patty = Ingredient(IngredientType.COOKED_PATTY)
        self.cooking = False
        self.image = self.__build_surface()

    def get_patty(self) -> Food or None:
        """
        Récupère une boulette qui est sur le grill sous forme de nourriture.
        :return: boulette s'il y en a une, None sinon
        """
        ingredient, self.__patty = self.__patty, None
        self.image = self.__build_surface()
        return ingredient

    def has_cooked_patty(self) -> bool:
        """
        Vérifie si une boulette cuite se trouve sur le grill.
        :return: True si une boulette cuite est sur le grill, False sinon
        """
        return not self.cooking and self.__patty

    def is_available(self) -> bool:
        """
        Vérifie si le grill est disponible pour la cuisson d'une nouvelle boulette.
        :return: True si on peut cuire une boulette, False sinon
        """
        return not self.cooking and not self.__patty

    def update(self):
        """ Met à jour l'apparence du grill en fonction de son état actuel. """
        if self.cooking:
            self.image = self.__build_surface()

    def __build_surface(self) -> pygame.Surface:
        """
        Construit l'image représentant le grill et son état.
        :return: image représentant le grill
        """
        surface = pygame.Surface((Grill.WIDTH, Grill.HEIGHT), flags=pygame.SRCALPHA)
        surface.fill(settings.GRILL_COLOR)

        for i in range(1, 5):
            rect = pygame.Rect(5, i * 10 - 2, 40, 5)
            pygame.draw.rect(surface, settings.GRILL_DARK_COLOR, rect)

        if self.__patty:
            pygame.draw.circle(surface, self.__patty_color, (25, 25), 16)

        return surface

    def __cook(self) -> None:
        """
        Procède à la cuisson de la boulette. Cette méthode modifie l'apparence de la boulette en cours de cuisson.
        :return: aucun
        """
        raw = settings.RAW_PATTY_COLOR
        red, green, blue = float(raw[0]), float(raw[1]), float(raw[2])
        cooked = settings.COOKED_PATTY_COLOR

        assert(red >= cooked[0] and green >= cooked[1] and blue >= cooked[2])

        red_step = float(red - cooked[0]) / Grill.COOKING_STEPS
        green_step = float(green - cooked[1]) / Grill.COOKING_STEPS
        blue_step = float(blue - cooked[2]) / Grill.COOKING_STEPS

        for _ in range(Grill.COOKING_STEPS):
            time.sleep(Grill.COOKING_TICK)
            red -= red_step
            green -= green_step
            blue -= blue_step
            color = round(red), round(green), round(blue)
            self.patty_color = color

        self.__cooking_done()

    @property
    def cooking(self) -> bool:
        return self.__cooking

    @property
    def patty_color(self) -> tuple:
        return self.__patty_color

    @cooking.setter
    def cooking(self, value: bool) -> None:
        self.__cooking = value

    @patty_color.setter
    def patty_color(self, color: tuple) -> None:
        self.__patty_color = color
