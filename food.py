from abc import ABC, abstractmethod

import pygame


class Food(ABC):
    """
    Nourriture.
    """

    def __init__(self):
        self.buffer_surface = None

    @abstractmethod
    def draw(self, surface: pygame.Surface, pos: tuple) -> None:
        pass

    @abstractmethod
    def height(self) -> int:
        pass

    @abstractmethod
    def width(self) -> int:
        pass

    @property
    def buffer(self):
        return self.buffer_surface
