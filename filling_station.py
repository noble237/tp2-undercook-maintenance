import threading
import time

import pygame

from beverage import Beverage, BeverageType
import settings


class FillingStation(pygame.sprite.Sprite):
    """
    Station de remplissage de boissons.
    """

    __STATE_NO_CUP = 0
    __STATE_FILLING = 1
    __STATE_BEVERAGE_READY = 2

    __FILLING_TIME = 4.00  # en secondes

    def __init__(self, beverage_type: BeverageType, pos: tuple) -> None:
        """
        Initialise la station de remplissage.
        :param beverage_type: type de boisson fournie par la station de remplissage
        :param pos: position de la station de remplissage à l'écran
        """
        super().__init__()

        self.__beverage = Beverage(beverage_type)
        self.__state = FillingStation.__STATE_NO_CUP

        self.image = self.__build_surface()

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def fill(self) -> None:
        """
        Débute le remplissage d'une boisson. Le remplissage prend un certain temps et n'est pas complété au retour
        de l'appel de cette méthode.
        :return: aucun
        """
        if self.__state == FillingStation.__STATE_NO_CUP:
            self.__state = FillingStation.__STATE_FILLING
            self.image = self.__build_surface()
            filling_thread = threading.Thread(target=self.__fill)
            filling_thread.start()

    def get_beverage(self) -> Beverage or None:
        """
        Récupère la boisson remplie si c'est possible.
        :return: la boisson si elle est prête, None sinon
        """
        if self.__state == FillingStation.__STATE_BEVERAGE_READY:
            self.__state = FillingStation.__STATE_NO_CUP
            self.image = self.__build_surface()
            return self.__beverage

        return None

    def is_available(self) -> bool:
        """
        Vérifie si la station de remplissage est disponible pour remplir une nouvelle boisson.
        :return: True si la station est disponible, False sinon
        """
        return self.__state == FillingStation.__STATE_NO_CUP

    def __build_surface(self) -> pygame.Surface:
        """
        Construit l'image représentant la station de remplissage dans son état actuel.
        :return: image de la station de remplissage
        """
        surface = pygame.Surface((50, 70), flags=pygame.SRCALPHA)
        surface.fill(settings.FILLING_STATION_COLOR)

        rect = pygame.Rect(5, 5, 40, 10)
        pygame.draw.rect(surface, self.__beverage.color(), rect)

        rect = pygame.Rect(5, 15, 40, 50)
        if self.__state != FillingStation.__STATE_BEVERAGE_READY:
            pygame.draw.rect(surface, settings.FILLING_STATION_DARK_COLOR, rect)
        else:
            pygame.draw.rect(surface, (0, 255, 0), rect)

        rect = pygame.Rect(22, 15, 6, 8)
        pygame.draw.rect(surface, settings.FILLING_STATION_NOZZLE_COLOR, rect)

        if self.__state != FillingStation.__STATE_NO_CUP:
            self.__beverage.draw(surface, (13, 24))

        return surface

    def __fill(self) -> None:
        """
        Procède au remplissage de la boisson.
        :return: aucun
        """
        time.sleep(FillingStation.__FILLING_TIME)

        self.__state = FillingStation.__STATE_BEVERAGE_READY
        self.image = self.__build_surface()
