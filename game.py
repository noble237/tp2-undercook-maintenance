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
import math

from cutting_station import CuttingStation



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
        self.__spacing = 55

        self.__trash = Trash((20, settings.SCREEN_HEIGHT - (Trash.HEIGHT + 20)))

        self.__platters_group = pygame.sprite.Group()
        self.__platters = [Platter((120, 200)), Platter((120, 300)), Platter((120, 400))]
        self.__platters_group.add(self.__platters)


    ########################################## C6 ##########################################

        self.__filling_stations_group = pygame.sprite.Group()
        liste_brevages = [
            BeverageType.COLA, BeverageType.ORANGE_SODA, BeverageType.LEMON_SODA,
            BeverageType.LEMONADE, BeverageType.PINK_LEMONADE
        ]
        self.__filling_stations = [
            FillingStation(liste_brevages[i], (((400 + 800) // 2) + (i - len(liste_brevages) // 2) * self.__spacing, 200))
            for i in range(len(liste_brevages))
        ]
        self.__filling_stations_group.add(self.__filling_stations)


        self.__fryers_group = pygame.sprite.Group()
        self.__fryers = [
            Fryer((settings.SCREEN_WIDTH - (Fryer.WIDTH + 200), ((317.5 + 400) // 2) + (i - 1) * self.__spacing))
            for i in range(2)
        ]
        self.__fryers_group.add(self.__fryers)

        self.__grills_group = pygame.sprite.Group()
        self.__grills = [
            Grill((settings.SCREEN_WIDTH - (Grill.WIDTH + 200), ((100 + 250) // 2) + (i - 1) * self.__spacing))
            for i in range(3)
        ]
        self.__grills_group.add(self.__grills)

    ########################################## C6 ##########################################

        self.__fridges_group = pygame.sprite.Group()
        liste_ingredients = [
            IngredientType.BOTTOM_BUN, IngredientType.TOP_BUN, IngredientType.RAW_PATTY,
            IngredientType.CHEESE_SLICE, IngredientType.UNPREPARED_ONION, IngredientType.UNPREPARED_LETTUCE,
            IngredientType.UNPREPARED_TOMATO, IngredientType.UNPREPARED_PICKLE, IngredientType.POTATO
        ]
        self.__fridges = [
            Fridge(Ingredient(liste_ingredients[i]), (((220 + 1020) // 2) + (i - len(liste_ingredients) // 2) * self.__spacing, settings.SCREEN_HEIGHT - 60))
            for i in range(len(liste_ingredients))
        ]
        self.__fridges_group.add(self.__fridges)

        self.__assembly_stations_group = pygame.sprite.Group()
        self.__assembly_stations = [AssemblyStation((400, 500)),
                                    AssemblyStation((500, 500)),
                                    AssemblyStation((600, 500)),
                                    AssemblyStation((700, 500)),
                                    AssemblyStation((800, 500))]
        self.__assembly_stations_group.add(self.__assembly_stations)

        self.__chef = Chef((screen.get_width() / 2, screen.get_height() / 2))

        self.__cutting_stations_group = pygame.sprite.Group()
        self.__cutting_stations = [
            CuttingStation((settings.SCREEN_WIDTH - (CuttingStation.WIDTH + 200), ((300 + 700) // 2) + (i - 1) * 70))
            for i in range(4)
        ]
        self.__cutting_stations_group.add(self.__cutting_stations)
        

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
        self.__fryers_group.update()
        self.__cutting_stations_group.update()
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
        self.__cutting_stations_group.draw(self.__screen)
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

    ########################################## C6 ##########################################

    def calculate_distance(self, pos1, pos2):
        """Calcule la distance entre deux points."""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def get_relevant_equipments(self):
        if self.__chef.has_potato_slices():
            return list(self.__fryers_group)
        elif self.__chef.has_raw_patty():
            return list(self.__grills_group)
        elif self.__chef.has_ingredient_for_cutting():
            return list(self.__cutting_stations_group)
        else:
            return list(self.__fryers_group) + list(self.__fryers_group) + \
                list(self.__fridges_group) + list(self.__filling_stations_group) + \
                list(self.__assembly_stations_group) + list(self.__platters_group) + \
                list(self.__cutting_stations_group) + [self.__trash]

    def get_closest_available_equipment(self, only_equipement):
        chef_pos = self.__chef.rect.center

        if only_equipement:
            relevant_equipments = only_equipement
        else:
            relevant_equipments = self.get_relevant_equipments()


        closest = None
        min_distance = float('inf')

        for equipment in relevant_equipments:
            distance = self.calculate_distance(chef_pos, equipment.rect.center)
            if distance < min_distance:
                if isinstance(equipment, (Fryer, Grill)) and not equipment.is_available():
                    continue
                min_distance = distance
                closest = equipment

        # Retourner la poubelle si aucun équipement disponible n'est trouvé pour des cas
        if closest is None and (self.__chef.has_potato_slices() or self.__chef.has_raw_patty()):
            return self.__trash
        else:
            return closest

    def interact_with_closest_equipment(self, equipment):
        if isinstance(equipment, FillingStation):
            self.interact_with_filling_station(equipment)
        elif isinstance(equipment, Fryer):
            self.interact_with_fryer(equipment)
        elif isinstance(equipment, Grill):
            self.interact_with_grill(equipment)
        elif isinstance(equipment, Fridge):
            self.interact_with_fridge(equipment)
        elif isinstance(equipment, AssemblyStation):
            self.interact_with_assembly_station(equipment)
        elif isinstance(equipment, Platter):
            self.interact_with_platter(equipment)
        elif isinstance(equipment, CuttingStation):
            self.interact_with_cutting_station(equipment)
        elif isinstance(equipment, Trash):
            self.interact_with_trash(self.__chef)

    def interact_with_filling_station(self, filling_station):
        if not self.__chef.food:
            if filling_station.is_available():
                self.__chef.drop_food()
                filling_station.fill()
            else:
                self.__chef.grab_food(filling_station.get_beverage())


    def interact_with_fryer(self, fryer):
        if fryer.is_available() and self.__chef.has_potato_slices():
            self.__chef.drop_food()
            fryer.fry()
        elif fryer.has_fryed_fries() and not self.__chef.food:
            food = fryer.get_fries()
            self.__chef.grab_food(food)
        elif fryer.has_overfryed_or_burnt_fries() and not self.__chef.food:
            food = fryer.get_fries()
            self.__chef.grab_food(food)
            self.__chef.drop_food()

    def interact_with_grill(self, grill):
        if grill.is_available() and self.__chef.has_raw_patty():
            food = self.__chef.drop_food()
            grill.cook(food)
        elif grill.has_cooked_patty() and not self.__chef.food:
            food = grill.get_patty()
            self.__chef.grab_food(food)
        elif grill.has_overcooked_or_burnt_patty() and not self.__chef.food:
            food = grill.get_patty()
            self.__chef.grab_food(food)
            self.__chef.drop_food()

    def interact_with_fridge(self, fridge):
        if self.__chef.food and fridge.can_return_ingredient(self.__chef.food):
            self.__chef.drop_food()
        else:
            if not self.__chef.food:
                self.__chef.grab_food(fridge.get_food())


    def interact_with_assembly_station(self, assembly_station):
        if self.__chef.food:
            if assembly_station.add_ingredient(self.__chef.food):
                self.__chef.drop_food()
        else:
            food = assembly_station.get_burger()
            self.__chef.grab_food(food)

    def interact_with_platter(self, platter):
        if self.__chef.food:
            if platter.add_food(self.__chef.food):
                self.__chef.drop_food()
        else:
            food = platter.get_meal()
            self.__chef.grab_food(food)

    def interact_with_trash(self, chef):
        chef.drop_food()

    def interact_with_orderboard(self, orderboard):
        self.__chef.deliver_meal(orderboard)


    def interact_with_cutting_station(self, cutting_station):
        if self.__chef.has_ingredient_for_cutting() and cutting_station.is_available():
            cutting_station.start_cutting(self.__chef.food)
            self.__chef.drop_food()
        elif cutting_station.is_ready():
            cut_ingredient = cutting_station.get_cut_ingredient()
            if cut_ingredient:
                self.__chef.grab_food(cut_ingredient)


    def __handle_pygame_events(self) -> None:
        """
        Gère les événements envoyés par Pygame.
        :return: aucun
        """
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                return

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.__running = False
                return

            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                self.__handle_keyboard_event(event)



    ########################################## C6 ##########################################

    ########################################## C3 et C6 ##########################################
    def __handle_keyboard_event(self, event: pygame.event.Event) -> None:
        """
        Gère les événements associés aux touches du clavier.
        :param event: événement du clavier
        :return: aucun
        """

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_s, pygame.K_DOWN]:
                self.is_moving_down = True
            elif event.key in [pygame.K_a, pygame.K_LEFT]:
                self.is_moving_left = True
            elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                self.is_moving_right = True
            elif event.key in [pygame.K_w, pygame.K_UP]:
                self.is_moving_up = True
            elif event.key == pygame.K_SPACE:
                self.handle_space_key()

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_s, pygame.K_DOWN]:
                self.is_moving_down = False
            elif event.key in [pygame.K_a, pygame.K_LEFT]:
                self.is_moving_left = False
            elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                self.is_moving_right = False
            elif event.key in [pygame.K_w, pygame.K_UP]:
                self.is_moving_up = False

        self.__update_chef_movement()
    
    def handle_space_key(self):
        interacted = False
        filling_station = pygame.sprite.spritecollideany(self.__chef, self.__filling_stations_group)
        fryer = pygame.sprite.spritecollideany(self.__chef, self.__fryers_group)
        grill = pygame.sprite.spritecollideany(self.__chef, self.__grills_group)
        fridge = pygame.sprite.spritecollideany(self.__chef, self.__fridges_group)
        assembly_station = pygame.sprite.spritecollideany(self.__chef, self.__assembly_stations_group)
        platter = pygame.sprite.spritecollideany(self.__chef, self.__platters_group)
        trash = pygame.sprite.collide_rect(self.__chef, self.__trash)
        cutting_station = pygame.sprite.spritecollideany(self.__chef, self.__cutting_stations_group)


        # Vérifier les interactions directes avec chaque type d'équipement
        if filling_station:
            self.interact_with_filling_station(filling_station)
            interacted = True
        elif fryer:
            self.interact_with_fryer(fryer)
            interacted = True
        elif grill:
            self.interact_with_grill(grill)
            interacted = True
        elif fridge:
            self.interact_with_fridge(fridge)
            interacted = True
        elif assembly_station:
            self.interact_with_assembly_station(assembly_station)
            interacted = True
        elif platter:
            self.interact_with_platter(platter)
            interacted = True
        elif trash:
            self.interact_with_trash(self.__chef)
            interacted = True
        elif cutting_station:
        ########################################## A5 ##########################################
            only_equipement = None
            if self.__chef.has_raw_patty():
                only_equipement = list(self.__grills_group)
            elif self.__chef.has_potato_slices():
                only_equipement = list(self.__fryers_group)

            if only_equipement:
                closest_equipment = self.get_closest_available_equipment(only_equipement)
                if closest_equipment:
                    self.interact_with_closest_equipment(closest_equipment)
            else:
                self.interact_with_cutting_station(cutting_station)
            interacted = True
        ########################################## A5 ##########################################

        else:
            self.interact_with_orderboard(self.__order_board)

        # Si aucune interaction directe n'a eu lieu, trouver l'équipement le plus proche
        if not interacted:
            closest_equipment = self.get_closest_available_equipment(None)
            if closest_equipment:
                self.interact_with_closest_equipment(closest_equipment)

    ########################################## C3 et C6 ##########################################

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