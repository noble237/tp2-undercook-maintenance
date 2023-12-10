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
    __STATE_OVERFRYING = 3
    __STATE_BURNT = 4

    __LED_COLORS = {
        __STATE_EMPTY_BASKET: (0, 0, 255),
        __STATE_FRYING: (255, 0, 0),
        __STATE_FRIES_READY: (0, 255, 0),
        __STATE_OVERFRYING: (100, 55, 0),
        __STATE_BURNT: (0, 0, 0)
    }

    __FRYING_TIME = 7.00  # en secondes
    __OVERFRYING_TIME = 10.00  # en secondes
    __OVERFRYING_STEPS = 30

    def __init__(self, pos: tuple) -> None:
        """
        Initialise la friteuse.
        :param pos: position de la friteuse à l'écran
        """
        super().__init__()

        self.__fries = None
        self.__state = Fryer.__STATE_EMPTY_BASKET
        self.image = self.__build_surface()
        
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def fry(self) -> None:
        """
        Commence à frire des frites. La cuisson (friture) prend un certain temps. 
        Les frites ne seront donc pas prêtes immédiatement après l'appel de cette méthode.
        """
        if self.__state == Fryer.__STATE_EMPTY_BASKET:
            self.__fries = Fries()

            self.__state = Fryer.__STATE_FRYING
            self.image = self.__build_surface()

            frying_thread = threading.Thread(target=self.__fry)
            frying_thread.start()

    def get_fries(self) -> Fries or None:
        """
        Récupère le cornet de frites si ces dernières sont prêtes ou brûlées.
        :return: le cornet de frites si elles sont prêtes, None sinon
        """
        if self.__state in [Fryer.__STATE_FRIES_READY, Fryer.__STATE_OVERFRYING, Fryer.__STATE_BURNT]:
            fries, self.__fries = self.__fries, None
            self.__state = Fryer.__STATE_EMPTY_BASKET
            self.image = self.__build_surface()
            return fries

        return None


    def is_available(self) -> bool:
        """
        Vérifie si la friteuse est disponible pour cuire de nouvelles frites.
        :return: True si on peut frire de nouvelles frites, False sinon
        """
        return not self.__fries and self.__state == Fryer.__STATE_EMPTY_BASKET
    

    def has_fryed_fries(self) -> bool:
        """
        Vérifie si les frites sont cuites et prêtes.
        :return: True si les frites sont cuites, False sinon
        """
        return self.__state == Fryer.__STATE_FRIES_READY

    def has_overfryed_or_burnt_fries(self) -> bool:
        """
        Vérifie si les frites sont surcuites ou brûlées.
        :return: True si les frites sont surcuites ou brûlées, False sinon
        """
        return self.__state in [Fryer.__STATE_OVERFRYING, Fryer.__STATE_BURNT]


    def update(self):
        """ Met à jour l'apparence des frites en fonction de son état actuel. """
        if self.__state:
            self.image = self.__build_surface()

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
        elif self.__fries and self.__state in [Fryer.__STATE_FRIES_READY, Fryer.__STATE_OVERFRYING, Fryer.__STATE_BURNT]:
            self.__fries.draw(surface, (12, 10))

        return surface


    def __fry(self) -> None:
        """
        Procède à la cuisson des frites.
        """
        time.sleep(Fryer.__FRYING_TIME)

        self.__state = Fryer.__STATE_FRIES_READY
        self.image = self.__build_surface()

        overfrying_thread = threading.Thread(target=self.__overfry)
        overfrying_thread.start()

    def __overfry(self) -> None:
        if self.__fries is None:
            return

        time.sleep(Fryer.__OVERFRYING_TIME)
        self.__state = Fryer.__STATE_OVERFRYING
        self.image = self.__build_surface()

        cooked = settings.FRIES_COLOR
        red, green, blue = float(cooked[0]), float(cooked[1]), float(cooked[2])
        burnt = settings.BURNT_FRIES_COLOR

        assert(red >= burnt[0] and green >= burnt[1] and blue >= burnt[2])

        red_step = (red - burnt[0]) / Fryer.__OVERFRYING_STEPS
        green_step = (green - burnt[1]) / Fryer.__OVERFRYING_STEPS
        blue_step = (blue - burnt[2]) / Fryer.__OVERFRYING_STEPS

        for _ in range(Fryer.__OVERFRYING_STEPS):
            if self.__fries is None:
                return

            time.sleep(Fryer.__OVERFRYING_TIME / Fryer.__OVERFRYING_STEPS)
            red -= red_step
            green -= green_step
            blue -= blue_step

            if self.__fries:
                self.__fries.color = (round(red), round(green), round(blue))
                self.image = self.__build_surface()

        if self.__fries:
            self.__state = Fryer.__STATE_BURNT
            self.image = self.__build_surface()
