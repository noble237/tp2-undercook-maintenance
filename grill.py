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
    COOKING_STEPS = 20

    OVERCOOKING_TICK = 0.10  # en secondes
    OVERCOOKING_STEPS = 100

    def __init__(self, pos: tuple) -> None:
        """
        Initialise le grill.
        :param pos: position du grill à l'écran
        """
        super().__init__()

        self.__cooking = False
        self.__overcooking = False
        self.__burnt = False

        self.__patty = None
        self.__patty_color = settings.RAW_PATTY_COLOR

        self.image = self.__build_surface()

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def reset(self):
        """
        Réinitialise le grill à son état initial.
        """

        self.__cooking = False
        self.__overcooking = False
        self.__burnt = False

        self.__patty = None
        self.__patty_color = settings.RAW_PATTY_COLOR

        self.image = self.__build_surface()

    ########################################## R1 ##########################################

    def start_cooking(self, ingredient: Ingredient):
        """ Commence à cuire un ingrédient. """
        if not self.is_available() or ingredient.ingredient_type() != IngredientType.RAW_PATTY:
            return False
        self.cook(ingredient)
        return True

    def get_cooked_patty(self):
        """ Récupère une boulette cuite si disponible. """
        if self.has_cooked_patty():
            return self.get_patty()
        return None

    def get_overcooked_or_burnt_patty(self):
        """ Récupère une boulette surcuite ou brûlée si disponible. """
        if self.has_overcooked_or_burnt_patty():
            return self.get_patty()
        return None

    ########################################## R1 ##########################################

    def cook(self, ingredient: Ingredient) -> None:
        """
        Débute la cuisson d'une boulette. Si l'ingrédient fourni n'est pas une boulette, rien ne se produit.
        La cuisson prend un certain temps. Elle ne sera pas complétée au retour de l'appel de cette méthode.
        :param ingredient: boulette de viande crue
        :return: aucun
        """
        if self.__cooking or self.__overcooking or self.__burnt:
            return

        if not ingredient or ingredient.ingredient_type() != IngredientType.RAW_PATTY:
            return

        self.cooking = True

        self.__patty = ingredient
        self.__patty_color = settings.RAW_PATTY_COLOR

        cooking_thread = threading.Thread(target=self.__cook)
        cooking_thread.start()


    def has_cooked_patty(self) -> bool:
        """
        Vérifie si une boulette cuite se trouve sur le grill.
        :return: True si une boulette cuite est sur le grill, False sinon
        """
        return not self.cooking and self.__patty and not self.__overcooking and not self.__burnt
    

    def has_overcooked_or_burnt_patty(self) -> bool:
        """
        Vérifie si une boulette est surcuite ou brûlée se trouve sur le grill.
        :return: True si une boulette surcuite ou brûlée est sur le grill, False sinon
        """
        return not self.cooking and self.__patty and self.__overcooking or self.__burnt


    def is_available(self) -> bool:
        """
        Vérifie si le grill est disponible pour la cuisson d'une nouvelle boulette.
        :return: True si on peut cuire une boulette, False sinon
        """
        return not self.__cooking and not self.__patty and not self.__overcooking and not self.__burnt
    

    def update(self):
        """ Met à jour l'apparence du grill en fonction de son état actuel. """
        if self.__cooking or self.__overcooking or self.__burnt:
            self.image = self.__build_surface()


    def get_patty(self) -> Food or None:
        if self.__patty:
            if self.__overcooking:
                self.__overcooking = False
            if self.__burnt:
                self.__burnt = False
            grilled_patty, self.__patty = self.__patty, None
            self.image = self.__build_surface()

            return grilled_patty
        
        return None


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


    def __cooking_done(self) -> None:
        """
        Finalise la cuisson d'une boulette.
        :return: aucun
        """
        self.patty_color = settings.COOKED_PATTY_COLOR
        self.__patty = Ingredient(IngredientType.COOKED_PATTY)
        self.cooking = False
        self.image = self.__build_surface()

        overcooking_thread = threading.Thread(target=self.__overcook)
        overcooking_thread.start()


    def __overcook(self) -> None:

        start_time = time.time()
        while time.time() - start_time < Grill.OVERCOOKING_TICK * Grill.OVERCOOKING_STEPS:
            if self.__patty is None:
                return
            time.sleep(Grill.OVERCOOKING_TICK)

        self.__overcooking = True

        cooked = settings.COOKED_PATTY_COLOR
        red, green, blue = float(cooked[0]), float(cooked[1]), float(cooked[2])
        burnt = settings.BURNT_PATTY_COLOR

        assert(red >= burnt[0] and green >= burnt[1] and blue >= burnt[2])

        red_step = (red - burnt[0]) / Grill.OVERCOOKING_STEPS
        green_step = (green - burnt[1]) / Grill.OVERCOOKING_STEPS
        blue_step = (blue - burnt[2]) / Grill.OVERCOOKING_STEPS

        for _ in range(Grill.OVERCOOKING_STEPS):
            if self.__patty is None:
                return

            time.sleep(Grill.OVERCOOKING_TICK)
            red -= red_step
            green -= green_step
            blue -= blue_step

            if self.__patty:
                self.patty_color = round(red), round(green), round(blue)

        if self.__patty:
            self.__burnt = True
            self.__overcooking_done()


    def __overcooking_done(self) -> None:
        """
        Finalise la surcuisson d'une boulette.
        :return: aucun
        """
        self.patty_color = settings.BURNT_PATTY_COLOR
        self.__patty = Ingredient(IngredientType.BURNT_PATTY)
        self.image = self.__build_surface()


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
