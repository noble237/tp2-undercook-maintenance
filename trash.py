import pygame

import settings


class Trash(pygame.sprite.Sprite):
    """
    Poubelle.
    """

    WIDTH = 32
    HEIGHT = 40

    def __init__(self, pos: tuple) -> None:
        """
        Initialise la poubelle.
        :param pos: position où afficher la poubelle à l'écran
        """
        super().__init__()

        self.image = Trash.__build_surface()

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.__sprite_group = pygame.sprite.GroupSingle()
        self.__sprite_group.add(self)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Dessine la poubelle sur la surface spécifiée.
        :param surface: surface sur laquelle dessiner la poubelle
        :return: aucun
        """
        self.__sprite_group.draw(surface)

    @staticmethod
    def __build_surface() -> pygame.Surface:
        """
        Construit l'image représentant la poubelle.
        :return: surface contenant l'image de la poubelle
        """
        surface = pygame.Surface((Trash.WIDTH, Trash.HEIGHT), flags=pygame.SRCALPHA)

        rect = pygame.Rect((2, 0), (28, 2))
        pygame.draw.rect(surface, settings.TRASH_COLOR, rect)
        rect = pygame.Rect((0, 2), (32, 38))
        pygame.draw.rect(surface, settings.TRASH_COLOR, rect)
        rect = pygame.Rect((6, 8), (20, 12))
        pygame.draw.rect(surface, (0, 0, 0), rect)

        return surface
