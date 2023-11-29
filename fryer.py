import threading
import time

import pygame

from fries import Fries
import settings


class Fryer(pygame.sprite.Sprite):
    """
    Friteuse pour frire les patates.
    """

    WIDTH = 50
    HEIGHT = 50

    __STATE_EMPTY_BASKET = 0
    __STATE_FRYING = 1
    __STATE_FRIES_READY = 2

    __LED_COLORS = {__STATE_EMPTY_BASKET: (50, 50, 50),
                    __STATE_FRYING: (255, 0, 0),
                    __STATE_FRIES_READY: (0, 255, 0)}

    __FRYING_TIME = 7.00  # en secondes

    def __init__(self, pos: tuple) -> None:
        """
        Initialise la friteuse.
        :param pos: position de la friteuse à l'écran
        """
        super().__init__()

        self.__fries = Fries()
        self.__state = Fryer.__STATE_EMPTY_BASKET

        self.image = self.__build_surface()

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def fry(self) -> None:
        """
        Commence à frire des frites. La cuisson (friture) prend un certain temps. Les frites ne seront donc
        pas prêtes immédiatement après l'appel de cette méthode.
        :return: aucun
        """
        if self.__state == Fryer.__STATE_EMPTY_BASKET:
            self.__state = Fryer.__STATE_FRYING
            self.image = self.__build_surface()
            frying_thread = threading.Thread(target=self.__fry)
            frying_thread.start()

    def get_fries(self) -> Fries or None:
        """
        Récupère le cornet de frites si ces dernières sont prêtes.
        :return: le cornet de frites si elles sont prêtes, None sinon
        """
        if self.__state == Fryer.__STATE_FRIES_READY:
            self.__state = Fryer.__STATE_EMPTY_BASKET
            self.image = self.__build_surface()
            return Fries()

        return None

    def is_available(self) -> bool:
        """
        Vérifie si la friteuse est disponible pour cuire de nouvelles frites.
        :return: True si on peut frire de nouvelles frites, False sinon
        """
        return self.__state == Fryer.__STATE_EMPTY_BASKET

    def __build_surface(self) -> pygame.Surface:
        """
        Construit l'image représentant la friteuse en fonction de son état.
        :return: l'image de la friteuse
        """
        surface = pygame.Surface((Fryer.WIDTH, Fryer.HEIGHT), flags=pygame.SRCALPHA)
        surface.fill(settings.FRYER_COLOR)

        color = Fryer.__LED_COLORS[self.__state]
        rect = pygame.Rect(43, 2, 5, 5)
        pygame.draw.rect(surface, color, rect)

        if self.__state == Fryer.__STATE_EMPTY_BASKET:
            rect = pygame.Rect(10, 10, 30, 30)
            pygame.draw.rect(surface, settings.FRYER_DARK_COLOR, rect)
        elif self.__state == Fryer.__STATE_FRYING:
            rect = pygame.Rect(10, 10, 30, 30)
            pygame.draw.rect(surface, settings.FRIES_COLOR, rect)
        elif self.__state == Fryer.__STATE_FRIES_READY:
            self.__fries.draw(surface, (12, 10))

        return surface

    def __fry(self) -> None:
        """
        Procède à la cuisson des frites.
        :return: aucun
        """
        time.sleep(Fryer.__FRYING_TIME)

        self.__state = Fryer.__STATE_FRIES_READY
        self.image = self.__build_surface()
