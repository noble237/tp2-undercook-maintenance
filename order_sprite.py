import pygame

from orders import Order
import settings


class OrderSprite(pygame.sprite.Sprite):
    """
    Sprite représentant une commande en attente.
    """
    __SPEED = 8

    def __init__(self, order: Order) -> None:
        """
        Initialise le sprite associé à la commande en paramètre.
        :param order: commande à afficher/animer
        """
        super().__init__()

        self.__order = order

        self.__time_percentage = order.get_remaining_time_percentage()
        self.__previous_time_percentage = self.__time_percentage + 1

        self.image = self.__build_surface()

        self.rect = self.image.get_rect()
        self.rect.x = settings.SCREEN_WIDTH  # s'affiche d'abord à droite (à l'extérieur) de l'écran
        self.rect.y = 10

        self.__left_align = settings.SCREEN_WIDTH

    def push_to(self, x: int) -> None:
        """
        Indique la position horizontale jusqu'où pousser le sprite vers la gauche.
        :param x: position à rejoindre
        :return: aucun
        """
        self.__left_align = x

    def update(self) -> None:
        """
        Met à jour le sprite: ajuste la position s'il doit être poussé et ajuste l'affichage
        du temps qui reste avant l'expiration de la commande.
        :return: aucun
        """
        if self.rect.x > self.__left_align:
            self.rect.x = max(self.__left_align, self.rect.x - OrderSprite.__SPEED)

        self.__time_percentage = self.__order.get_remaining_time_percentage()
        if self.__time_percentage != self.__previous_time_percentage:
            self.__previous_time_percentage = self.__time_percentage
            self.image = self.__build_surface()

    def __build_surface(self) -> pygame.Surface:
        """
        Construit l'image représentant la commande. Va inclure le contenu de la commande et un
        indicateur du temps qui reste avant son expiration.
        :return: l'image construite
        """
        surface = pygame.Surface((60, 70), flags=pygame.SRCALPHA)
        surface.fill((250, 255, 225))

        self.__draw_beverage(surface)
        self.__draw_fries(surface)

        burger = self.__order.burger
        x = (surface.get_width() - 32) / 2
        y = surface.get_height() - 4 - burger.height()
        burger.draw(surface, (x, y))

        rect = pygame.Rect(4, 4, 52, 10)
        pygame.draw.rect(surface, (0, 0, 0), rect)
        w = round(48 * self.__time_percentage / 100.0)
        rect = pygame.Rect(6, 6, w, 6)
        pygame.draw.rect(surface, (0, 255, 0), rect)
        return surface

    def __draw_beverage(self, surface: pygame.Surface) -> None:
        """
        Dessine (ou pas) la boisson sur la surface spécifiée.
        :param surface: surface sur laquelle dessiner la boisson
        :return: aucun
        """
        if self.__order.beverage is None:
            return

        x = (surface.get_width() - 32) / 2 - 8
        y = surface.get_height() - 54

        beverage = self.__order.beverage
        beverage.draw(surface, (x, y))

    def __draw_fries(self, surface: pygame.Surface) -> None:
        """
        Dessine (ou pas) le cornet de frites sur la surface spécifiée.
        :param surface: surface sur laquelle dessiner le cornet de frites
        :return: aucun
        """
        if self.__order.fries is None:
            return

        x = (surface.get_width() - 32) / 2 + 14
        y = surface.get_height() - 46

        fries = self.__order.fries
        fries.draw(surface, (x, y))

    @property
    def order(self) -> Order:
        return self.__order
