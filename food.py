from abc import ABC, abstractmethod

import pygame


class Food(ABC):
    """
    Nourriture.
    """

    @abstractmethod
    def draw(self, surface: pygame.Surface, pos: tuple) -> None:
        pass

    @abstractmethod
    def height(self) -> int:
        pass

    @abstractmethod
    def width(self) -> int:
        pass
