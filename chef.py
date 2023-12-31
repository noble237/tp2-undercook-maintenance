import pygame
import settings
from typing import Union, List
from food import Food
from ingredients import Ingredient, IngredientType
from meal import Meal
from order_board import OrderBoard
from orders import Order


class Chef(pygame.sprite.Sprite):
    """
    Chef cuisinier contrôlé par le joueur.
    """

    __FACING_UP = 0
    __FACING_RIGHT = 1
    __FACING_DOWN = 2
    __FACING_LEFT = 3

    __SPEED = 3

    def __init__(self, pos: tuple) -> None:
        """
        Initialise le chef cuisinier.
        :param pos: position du chef cuisinier à l'écran
        """
        super().__init__()

        self.__facing = Chef.__FACING_DOWN
        self.__walking = 0, 0

        self.__food = None  # nourriture transportée par le chef cuisinier

        self.is_moving_up = False
        self.is_moving_down = False
        self.is_moving_left = False
        self.is_moving_right = False

        self.__surfaces = self.__build_surfaces()
        self.image = self.__surfaces[self.__facing]

        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - self.rect.width / 2
        self.rect.y = pos[1] - self.rect.height / 2

        self.__sprite_group = pygame.sprite.GroupSingle()
        self.__sprite_group.add(self)

    def reset(self):
        """
        Réinitialise le chef à son état initial.
        """

        self.drop_food()
        self.rect.x, self.rect.y = self.__initial_position

        self.is_moving_left = self.is_moving_right = False
        self.is_moving_up = self.is_moving_down = False

    
    def reset(self, initial_position: tuple):
        """
        Réinitialise le chef à son état initial.
        :param initial_position: position initiale du chef à l'écran
        """

        self.rect.x, self.rect.y = initial_position

        self.__facing = Chef.__FACING_DOWN
        self.is_moving_up = self.is_moving_down = False
        self.is_moving_left = self.is_moving_right = False
        self.drop_food()

        self.image = self.__surfaces[self.__facing]

    ########################################## C1 ##########################################

    def deliver_meal(self, order_board: OrderBoard) -> Order or None:
        """
        Livre un repas.
        :param order_board: le tableau des commandes en attente
        :return: la commande si la livraison est réussie, None sinon
        """

        if not self.__food:
            return None

        if not isinstance(self.__food, Meal):
            return None

        order = order_board.collides_with(self)
        if order and self.matches_order(self.__food, order):
            order_board.remove_order(order.order_id)
            self.drop_food()
            return order

        return None


    def matches_order(self, meal: Meal, order: Order) -> bool:
        """
        Vérifie si le repas correspond à la commande.
        :param meal: le repas à vérifier
        :param order: la commande à comparer
        :return: True si le repas correspond à la commande, False sinon
        """
        # Comparaison Burger
        if meal.burger is None or order.burger is None:
            if meal.burger is not None or order.burger is not None:
                return False  # Un a un burger et l'autre non
        else:
            types_meal_burger = {ingredient.ingredient_type() for ingredient in meal.burger.ingredients}
            types_order_burger = {ingredient.ingredient_type() for ingredient in order.burger.ingredients}
            if types_meal_burger != types_order_burger:
                return False  # Ingrédients du burger ne correspondent pas

        # Comparaison Frites
        if (meal.fries is None) != (order.fries is None):
            return False  # Une des commandes a des frites et l'autre non

        # Comparaison Beverage
        if meal.beverage is None or order.beverage is None:
            if meal.beverage is not None or order.beverage is not None:
                return False  # Une a une boisson et l'autre non
        else:
            if meal.beverage.color() != order.beverage.color():
                return False  # Couleurs des boissons ne correspondent pas

        return True

    ########################################## C1 ##########################################

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

    ########################################## R2 ##########################################

    def has_ingredient(self, ingredient_type: Union[IngredientType, List[IngredientType]]) -> bool:
        """
        Vérifie si le chef tient un ou plusieurs ingrédients spécifiques.
        :param ingredient_type: Le type d'ingrédient ou une liste de types d'ingrédients à vérifier.
        :return: True si le chef tient l'un des ingrédients spécifiés, False sinon.
        """
        if not self.__food:
            return False

        if not isinstance(self.__food, Ingredient):
            return False

        if isinstance(ingredient_type, IngredientType):
            return self.__food.ingredient_type() == ingredient_type
        elif isinstance(ingredient_type, list):
            return self.__food.ingredient_type() in ingredient_type

        return False
    
    ########################################## R2 ##########################################


    def move_horizontal(self, direction):
        """
        Déplace le chef horizontalement.
        :param direction: -1 pour gauche, 1 pour droite
        """
        self.__walking = direction, self.__walking[1]
        if direction != 0:
            self.__facing = Chef.__FACING_LEFT if direction < 0 else Chef.__FACING_RIGHT

    def move_vertical(self, direction):
        """
        Déplace le chef verticalement.
        :param direction: -1 pour haut, 1 pour bas
        """
        self.__walking = self.__walking[0], direction
        if direction != 0:
            self.__facing = Chef.__FACING_UP if direction < 0 else Chef.__FACING_DOWN


    ########################################## C2 et C3 ##########################################

    def update(self):
        """
        Ajuste l'apparence et la position du chef cuisinier.
        """
        new_x = self.rect.x + self.__walking[0] * self.__SPEED
        new_y = self.rect.y + self.__walking[1] * self.__SPEED

    ########################################## C2 ##########################################
        # Limiter le mouvement pour empêcher le chef de sortir de l'écran
        if 0 <= new_x <= settings.SCREEN_WIDTH - self.rect.width:
            self.rect.x = new_x
        if 0 <= new_y <= settings.SCREEN_HEIGHT - self.rect.height:
            self.rect.y = new_y

    ########################################## C2 ##########################################

        if self.__walking[0] < 0:
            self.__facing = Chef.__FACING_LEFT
        elif self.__walking[0] > 0:
            self.__facing = Chef.__FACING_RIGHT
        elif self.__walking[1] < 0:
            self.__facing = Chef.__FACING_UP
        elif self.__walking[1] > 0:
            self.__facing = Chef.__FACING_DOWN

        self.image = self.__surfaces[self.__facing]

    ########################################## C2 et C3 ##########################################


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


    @property
    def food(self) -> Food or None:
        return self.__food

    @property
    def is_moving_up(self):
        return self._is_moving_up

    @is_moving_up.setter
    def is_moving_up(self, value):
        self._is_moving_up = value

    @property
    def is_moving_down(self):
        return self._is_moving_down

    @is_moving_down.setter
    def is_moving_down(self, value):
        self._is_moving_down = value

    @property
    def is_moving_left(self):
        return self._is_moving_left

    @is_moving_left.setter
    def is_moving_left(self, value):
        self._is_moving_left = value

    @property
    def is_moving_right(self):
        return self._is_moving_right

    @is_moving_right.setter
    def is_moving_right(self, value):
        self._is_moving_right = value