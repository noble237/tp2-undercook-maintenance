import pygame

import settings
from assembly_station import AssemblyStation
from filling_station import FillingStation
from fridge import Fridge
from fryer import Fryer
from grill import Grill
from platter import Platter
from trash import Trash
from chef import Chef
from order_board import OrderBoard

from beverage import BeverageType
from ingredients import Ingredient, IngredientType

import orders


class Game:
    """
    Partie. Cette classe gère les événements et interactions du jeu.
    """

    __MAX_FPS = 90
    __DEFAULT_FONT_SIZE = 20

    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initialise une partie.
        :param screen: écran où afficher le jeu
        """
        self.__screen = screen
        self.__running = False

    ########################################## C3 ##########################################

        self.is_moving_up = False
        self.is_moving_down = False
        self.is_moving_left = False
        self.is_moving_right = False

    ########################################## C3 ##########################################


        default_font_name = pygame.font.get_default_font()
        self.__font = pygame.font.Font(default_font_name, Game.__DEFAULT_FONT_SIZE)

        self.__clock = pygame.time.Clock()

        orders.init()
        self.__order_board = OrderBoard()

        self.__colliding = []

        self.__trash = Trash((20, settings.SCREEN_HEIGHT - (Trash.HEIGHT + 20)))

        self.__platters_group = pygame.sprite.Group()
        self.__platters = [Platter((120, 200)), Platter((120, 300)), Platter((120, 400))]
        self.__platters_group.add(self.__platters)

        self.__filling_stations_group = pygame.sprite.Group()
        self.__filling_stations = [FillingStation(BeverageType.COLA, (400, 200)),
                                   FillingStation(BeverageType.ORANGE_SODA, (500, 200)),
                                   FillingStation(BeverageType.LEMON_SODA, (600, 200)),
                                   FillingStation(BeverageType.LEMONADE, (700, 200)),
                                   FillingStation(BeverageType.PINK_LEMONADE, (800, 200))]
        self.__filling_stations_group.add(self.__filling_stations)

        self.__fryers_group = pygame.sprite.Group()
        self.__fryers = [Fryer((settings.SCREEN_WIDTH - (Fryer.WIDTH + 200), 400)),
                         Fryer((settings.SCREEN_WIDTH - (Fryer.WIDTH + 200), 475))]
        self.__fryers_group.add(self.__fryers)

        self.__grills_group = pygame.sprite.Group()
        self.__grills = [Grill((settings.SCREEN_WIDTH - (Grill.WIDTH + 200), 150)),
                         Grill((settings.SCREEN_WIDTH - (Grill.WIDTH + 200), 225)),
                         Grill((settings.SCREEN_WIDTH - (Grill.WIDTH + 200), 300))]
        self.__grills_group.add(self.__grills)

        self.__fridges_group = pygame.sprite.Group()
        self.__fridges = [Fridge(Ingredient(IngredientType.BOTTOM_BUN), (220, settings.SCREEN_HEIGHT - 60)),
                          Fridge(Ingredient(IngredientType.TOP_BUN), (320, settings.SCREEN_HEIGHT - 60)),
                          Fridge(Ingredient(IngredientType.RAW_PATTY), (420, settings.SCREEN_HEIGHT - 60)),
                          Fridge(Ingredient(IngredientType.CHEESE_SLICE), (520, settings.SCREEN_HEIGHT - 60)),
                          Fridge(Ingredient(IngredientType.ONION_SLICES), (620, settings.SCREEN_HEIGHT - 60)),
                          Fridge(Ingredient(IngredientType.LETTUCE_SLICES), (720, settings.SCREEN_HEIGHT - 60)),
                          Fridge(Ingredient(IngredientType.TOMATO_SLICES), (820, settings.SCREEN_HEIGHT - 60)),
                          Fridge(Ingredient(IngredientType.PICKLE_SLICE), (920, settings.SCREEN_HEIGHT - 60)),
                          Fridge(Ingredient(IngredientType.POTATO), (1020, settings.SCREEN_HEIGHT - 60))]
        self.__fridges_group.add(self.__fridges)

        self.__assembly_stations_group = pygame.sprite.Group()
        self.__assembly_stations = [AssemblyStation((400, 500)),
                                    AssemblyStation((500, 500)),
                                    AssemblyStation((600, 500)),
                                    AssemblyStation((700, 500)),
                                    AssemblyStation((800, 500))]
        self.__assembly_stations_group.add(self.__assembly_stations)

        self.__chef = Chef((screen.get_width() / 2, screen.get_height() / 2))

    def run(self) -> None:
        """ Boucle de jeu. """

        orders.spawner.start()

        self.__running = True
        while self.__running:
            self.__clock.tick(Game.__MAX_FPS)  # limite le nombre de trames par seconde
            self.__update()
            self.__draw()

        orders.spawner.stop()

    def __update(self) -> None:
        """ Mises à jour à effectuer à chaque trame. """
        self.__handle_pygame_events()
        self.__handle_orders()

        self.__order_board.update()
        self.__grills_group.update()
        self.__chef.update()

    def __draw(self) -> None:
        """ Dessins à effectuer à chaque trame. """
        self.__screen.fill((0, 120, 200))

        self.__trash.draw(self.__screen)

        self.__platters_group.draw(self.__screen)
        self.__filling_stations_group.draw(self.__screen)
        self.__fryers_group.draw(self.__screen)
        self.__grills_group.draw(self.__screen)
        self.__fridges_group.draw(self.__screen)
        self.__assembly_stations_group.draw(self.__screen)
        self.__order_board.draw(self.__screen)
        self.__chef.draw(self.__screen)
        # self.__show_fps()

        pygame.display.flip()

    def __show_fps(self) -> None:
        """ Affiche le nombre de trames par seconde (FPS). """
        info = f"{round(self.__clock.get_fps())} FPS"
        text_surface = self.__font.render(info, True, (255, 255, 255))
        pos = self.__screen.get_width() - text_surface.get_width() - 10, 10
        self.__screen.blit(text_surface, pos)

    def __handle_orders(self) -> None:
        """
        Ajoute les nouvelles commandes au tableau d'affichage des commandes.
        :return: aucun
        """
        if new_orders := orders.spawner.get():
            self.__order_board.add_orders(new_orders)
            for order in new_orders:
                order.start()

    def __handle_pygame_events(self) -> None:
        """
        Gère les événements envoyés par Pygame.
        :return: aucun
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                return

            # interception de la touche ESCAPE à ce niveau-ci pour arrêter la boucle au besoin
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.__running = False
                return

            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                self.__handle_keyboard_event(event)

    def __handle_keyboard_event(self, event: pygame.event.Event) -> None:
        """
        Gère les événements associés aux touches du clavier.
        :param event: événement du clavier
        :return: aucun
        """
    ########################################## C3 ##########################################

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_s, pygame.K_DOWN]:
                self.is_moving_down = True
            if event.key in [pygame.K_a, pygame.K_LEFT]:
                self.is_moving_left = True
            if event.key in [pygame.K_d, pygame.K_RIGHT]:
                self.is_moving_right = True
            if event.key in [pygame.K_w, pygame.K_UP]:
                self.is_moving_up = True

    ########################################## C3 ##########################################

            if event.key == pygame.K_SPACE:
                if filling_station := pygame.sprite.spritecollideany(self.__chef, self.__filling_stations_group):
                    if not self.__chef.food:
                        if filling_station.is_available():
                            self.__chef.drop_food()
                            filling_station.fill()
                        else:
                            self.__chef.grab_food(filling_station.get_beverage())
                elif fryer := pygame.sprite.spritecollideany(self.__chef, self.__fryers_group):
                    if fryer.is_available() and self.__chef.has_potato():
                        self.__chef.drop_food()
                        fryer.fry()
                    elif not self.__chef.food:
                        self.__chef.grab_food(fryer.get_fries())
                elif grill := pygame.sprite.spritecollideany(self.__chef, self.__grills_group):
                    if grill.is_available() and self.__chef.has_raw_patty():
                        food = self.__chef.drop_food()
                        grill.cook(food)
                    elif grill.has_cooked_patty() and not self.__chef.food:
                        food = grill.get_patty()
                        self.__chef.grab_food(food)
                elif fridge := pygame.sprite.spritecollideany(self.__chef, self.__fridges_group):
                    self.__chef.grab_food(fridge.get_food())
                elif assembly_station := pygame.sprite.spritecollideany(self.__chef, self.__assembly_stations_group):
                    if self.__chef.food:
                        if assembly_station.add_ingredient(self.__chef.food):
                            self.__chef.drop_food()
                    else:
                        food = assembly_station.get_burger()
                        self.__chef.grab_food(food)
                elif platter := pygame.sprite.spritecollideany(self.__chef, self.__platters_group):
                    if self.__chef.food:
                        if platter.add_food(self.__chef.food):
                            self.__chef.drop_food()
                    else:
                        food = platter.get_meal()
                        self.__chef.grab_food(food)
                elif pygame.sprite.collide_rect(self.__chef, self.__trash):
                    self.__chef.drop_food()
                else:
                    self.__chef.deliver_meal(self.__order_board)

    ########################################## C3 ##########################################

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_s, pygame.K_DOWN]:
                self.is_moving_down = False
            if event.key in [pygame.K_a, pygame.K_LEFT]:
                self.is_moving_left = False
            if event.key in [pygame.K_d, pygame.K_RIGHT]:
                self.is_moving_right = False
            if event.key in [pygame.K_w, pygame.K_UP]:
                self.is_moving_up = False

        self.__update_chef_movement()


    ########################################## C3 ##########################################

    def __update_chef_movement(self):
        if self.is_moving_left:
            self.__chef.move_horizontal(-1)
        elif self.is_moving_right:
            self.__chef.move_horizontal(1)
        else:
            self.__chef.move_horizontal(0)

        if self.is_moving_up:
            self.__chef.move_vertical(-1)
        elif self.is_moving_down:
            self.__chef.move_vertical(1)
        else:
            self.__chef.move_vertical(0)

    ########################################## C3 ##########################################