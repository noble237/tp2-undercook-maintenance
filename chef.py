import pygame

import settings

from food import Food
from ingredients import Ingredient, IngredientType
from meal import Meal
from order_board import OrderBoard


class Chef(pygame.sprite.Sprite):
    """
    Chef cuisinier contrôlé par le joueur.
    """

    __FACING_UP = 0
    __FACING_RIGHT = 1
    __FACING_DOWN = 2
    __FACING_LEFT = 3

    __SPEED = 2

    def __init__(self, pos: tuple) -> None:
        """
        Initialise le chef cuisinier.
        :param pos: position du chef cuisinier à l'écran
        """
        super().__init__()

        self.__facing = Chef.__FACING_DOWN
        self.__walking = 0, 0

        self.__food = None  # nourriture transportée par le chef cuisinier

        self.__surfaces = self.__build_surfaces()
        self.image = self.__surfaces[self.__facing]

        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - self.rect.width / 2
        self.rect.y = pos[1] - self.rect.height / 2

        self.__sprite_group = pygame.sprite.GroupSingle()
        self.__sprite_group.add(self)

    def deliver_meal(self, order_board: OrderBoard) -> bool:
        """
        Livre un repas.
        :param order_board: le tableau des commandes en attente
        :return: True si la livraison est réussie, False sinon
        """
        if not self.__food:
            return False

        if not isinstance(self.__food, Meal):
            return False

        if order := order_board.collides_with(self):
            order_board.remove_order(order.order_id)
            self.drop_food()
            return True

        return False

    def draw(self, surface: pygame.Surface) -> None:
        """
        Dessine le chef cuisinier sur la surface spécifiée.
        :param surface: surface sur laquelle dessiner le chef cuisinier
        :return: aucun
        """
        self.__sprite_group.draw(surface)

    def drop_food(self) -> Food or None:
        """
        Abandonne la nourriture transportée.
        :return: nourriture abandonnée ou None si le cuisinier n'en avait pas
        """
        food, self.__food = self.__food, None
        self.__surfaces = self.__build_surfaces()
        return food

    def grab_food(self, food: Food) -> None:
        """
        Ramasse (et transporte) la nourriture spécifiée en paramètre.
        :param food: nourriture à transporter
        :return: aucun
        """
        if not self.__food:
            self.__food = food
            self.__surfaces = self.__build_surfaces(self.__food)

    def has_potato(self) -> bool:
        """
        Vérifie si le chef cuisinier tient une patate dans ses mains.
        :return: True si le chef cuisinier tient une patate, False sinon
        """
        if not self.__food:
            return False

        if not isinstance(self.__food, Ingredient):
            return False

        return self.__food.ingredient_type() == IngredientType.POTATO

    def has_raw_patty(self) -> bool:
        """
        Vérifie si le chef cuisinier tient une boulette de viande crue dans ses mains.
        :return: True si le chef cuisinier tient une boulette de viande crue, False sinon
        """
        if not self.__food:
            return False

        if not isinstance(self.__food, Ingredient):
            return False

        return self.__food.ingredient_type() == IngredientType.RAW_PATTY

    def stop_walking_down(self) -> None:
        """
        Arrête le déplacement du chef cuisinier en direction du bas de l'écran.
        :return: aucun
        """
        self.__walking = self.__walking[0], 0

    def stop_walking_left(self) -> None:
        """
        Arrête le déplacement du chef cuisinier en direction de la gauche de l'écran.
        :return: aucun
        """
        self.__walking = 0, self.__walking[1]

    def stop_walking_right(self) -> None:
        """
        Arrête le déplacement du chef cuisinier en direction de la droite de l'écran.
        :return: aucun
        """
        self.__walking = 0, self.__walking[1]

    def stop_walking_up(self) -> None:
        """
        Arrête le déplacement du chef cuisinier en direction du haut de l'écran.
        :return: aucun
        """
        self.__walking = self.__walking[0], 0

    def update(self) -> None:
        """
        Ajuste l'apparence et la position du chef cuisinier.
        :return: aucun
        """
        self.image = self.__surfaces[self.__facing]
        self.__walk()

    def walk_down(self) -> None:
        """
        Initie un déplacement du chef cuisinier vers le bas de l'écran.
        :return: aucun
        """
        self.__facing = Chef.__FACING_DOWN
        self.__walking = self.__walking[0], 1

    def walk_left(self) -> None:
        """
        Initie un déplacement du chef cuisinier vers la gauche de l'écran.
        :return: aucun
        """
        self.__facing = Chef.__FACING_LEFT
        self.__walking = -1, self.__walking[1]

    def walk_right(self) -> None:
        """
        Initie un déplacement du chef cuisinier vers la droite de l'écran.
        :return: aucun
        """
        self.__facing = Chef.__FACING_RIGHT
        self.__walking = 1, self.__walking[1]

    def walk_up(self) -> None:
        """
        Initie un déplacement du chef cuisinier vers le haut de l'écran.
        :return: aucun
        """
        self.__facing = Chef.__FACING_UP
        self.__walking = self.__walking[0], -1

    @staticmethod
    def __build_surfaces(food: Food = None) -> list:
        """
        Construit les images représentant le chef cuisinier dans les 4 directions.
        La nourriture transportée, s'il y a lieu, est également ajoutée aux images.
        :param food: nourriture à ajouter aux images (None si rien à ajouter)
        :return: liste des images construites
        """
        surfaces_rect = pygame.Rect(0, 0, 40, 40)
        surfaces = [pygame.Surface(surfaces_rect.size, flags=pygame.SRCALPHA).convert_alpha() for _ in range(4)]

        if food:
            x = surfaces_rect.width - food.width()
            y = (surfaces_rect.height - food.height()) / 2
            food.draw(surfaces[Chef.__FACING_UP], (x, y))

        uniform_rect = pygame.Rect(4, 4, 32, 32)
        pygame.draw.rect(surfaces[Chef.__FACING_UP], settings.UNIFORM_COLOR, uniform_rect)
        hair_rect = pygame.Rect(4, 14, 32, 14)
        pygame.draw.rect(surfaces[Chef.__FACING_UP], settings.HAIR_COLOR, hair_rect)

        pygame.draw.rect(surfaces[Chef.__FACING_RIGHT], settings.UNIFORM_COLOR, uniform_rect)
        hair_rect = pygame.Rect(4, 14, 16, 14)
        pygame.draw.rect(surfaces[Chef.__FACING_RIGHT], settings.HAIR_COLOR, hair_rect)
        skin_rect = pygame.Rect(20, 14, 16, 14)
        pygame.draw.rect(surfaces[Chef.__FACING_RIGHT], settings.SKIN_COLOR, skin_rect)

        pygame.draw.rect(surfaces[Chef.__FACING_DOWN], settings.UNIFORM_COLOR, uniform_rect)
        hair_rect = pygame.Rect(4, 14, 32, 14)
        pygame.draw.rect(surfaces[Chef.__FACING_DOWN], settings.HAIR_COLOR, hair_rect)
        skin_rect = pygame.Rect(8, 14, 24, 14)
        pygame.draw.rect(surfaces[Chef.__FACING_DOWN], settings.SKIN_COLOR, skin_rect)

        if food:
            x = surfaces_rect.width - food.width()
            y = (surfaces_rect.height - food.height()) / 2
            food.draw(surfaces[Chef.__FACING_RIGHT], (x, y))
            x = 0
            food.draw(surfaces[Chef.__FACING_DOWN], (x, y))
            food.draw(surfaces[Chef.__FACING_LEFT], (x, y))

        pygame.draw.rect(surfaces[Chef.__FACING_LEFT], settings.UNIFORM_COLOR, uniform_rect)
        hair_rect = pygame.Rect(20, 14, 16, 14)
        pygame.draw.rect(surfaces[Chef.__FACING_LEFT], settings.HAIR_COLOR, hair_rect)
        skin_rect = pygame.Rect(4, 14, 16, 14)
        pygame.draw.rect(surfaces[Chef.__FACING_LEFT], settings.SKIN_COLOR, skin_rect)

        return surfaces

    def __walk(self) -> None:
        """
        Recalcule la position en fonction des déplacements demandés et de la vitesse de déplacement.
        :return: aucun
        """
        self.rect.x += self.__walking[0] * self.__SPEED
        self.rect.y += self.__walking[1] * self.__SPEED

    @property
    def food(self) -> Food or None:
        return self.__food
