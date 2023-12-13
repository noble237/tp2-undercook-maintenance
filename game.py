import pygame
import settings
import orders
import math
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
            FillingStation(liste_brevages[i], (((400 + 800) / 2) + (i - len(liste_brevages) / 2) * self.__spacing, 200))
            for i in range(len(liste_brevages))
        ]
        self.__filling_stations_group.add(self.__filling_stations)


        self.__fryers_group = pygame.sprite.Group()
        self.__fryers = [
            Fryer((settings.SCREEN_WIDTH - (Fryer.WIDTH + 200), ((317.5 + 400) / 2) + (i - 1) * self.__spacing))
            for i in range(2)
        ]
        self.__fryers_group.add(self.__fryers)

        self.__grills_group = pygame.sprite.Group()
        self.__grills = [
            Grill((settings.SCREEN_WIDTH - (Grill.WIDTH + 200), ((100 + 250) / 2) + (i - 1) * self.__spacing))
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
            Fridge(Ingredient(liste_ingredients[i]), (((220 + 1020) / 2) + (i - len(liste_ingredients) / 2) * self.__spacing, settings.SCREEN_HEIGHT - 60))
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


        self.__cutting_stations_group = pygame.sprite.Group()
        self.__cutting_stations = [
            CuttingStation((settings.SCREEN_WIDTH - (CuttingStation.WIDTH + 200), ((300 + 700) / 2) + (i - 1) * 70))
            for i in range(4)
        ]
        self.__cutting_stations_group.add(self.__cutting_stations)

        self.__chef_one = Chef((screen.get_width() * (1.9/4), screen.get_height() * (2/4)))
        self.__chef_two = Chef((screen.get_width() * (2.1/4), screen.get_height() * (2/4)))
        self.__chef = self.__chef_one

        self.__chef_controls = {
            pygame.K_DOWN: (self.__chef_one, 'down'),
            pygame.K_LEFT: (self.__chef_one, 'left'),
            pygame.K_RIGHT: (self.__chef_one, 'right'),
            pygame.K_UP: (self.__chef_one, 'up'),
            pygame.K_s: (self.__chef_two, 'down'),
            pygame.K_a: (self.__chef_two, 'left'),
            pygame.K_d: (self.__chef_two, 'right'),
            pygame.K_w: (self.__chef_two, 'up')
        }

        self.total_tips = 0
        self.__missed_orders = 0


    def run(self) -> bool:
        """ Boucle de jeu. Retourne True si le joueur veut quitter, False pour redémarrer. """

        orders.spawner.start()

        self.__running = True
        while self.__running:
            self.__clock.tick(Game.__MAX_FPS)  # limite le nombre de trames par seconde
            self.__update()
            self.__draw()

        orders.spawner.stop()
        return self.user_requested_quit()


    def __update(self) -> None:
        """ Mises à jour à effectuer à chaque trame. """
        self.__handle_pygame_events()
        self.__handle_orders()

        self.__order_board.update()
        self.__grills_group.update()
        self.__fryers_group.update()
        self.__cutting_stations_group.update()
        self.__chef_one.update()
        self.__chef_two.update()

        expired_orders = self.__order_board.get_expired_orders()
        for _ in expired_orders:
            self.__missed_orders += 1
            if self.__missed_orders >= 3:
                self.__show_game_over_screen()
                self.__reset_game()


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
        self.__chef_one.draw(self.__screen)
        self.__chef_two.draw(self.__screen)
        self.__show_fps()
        self.__draw_tips()
        self.__draw_hearts()
        
        pygame.display.flip()


    def __draw_tips(self):
        """ Affiche le total de pourboire(s) avec un contour noir et un remplissage blanc. """

        tip_info = f"Total de pourboire(s): {self.total_tips:.2f}$"
        text_surface = self.__font.render(tip_info, True, (255, 255, 255))
        text_x = self.__screen.get_width() / 2 - text_surface.get_width() / 2
        text_y = 10

        # Dessiner le contour en noir
        outline_color = (0, 0, 0)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    self.__screen.blit(self.__font.render(tip_info, True, outline_color), (text_x + dx, text_y + dy))

        self.__screen.blit(text_surface, (text_x, text_y))

    def __draw_hearts(self):
        """ Affiche les cœurs pour les vies restantes. """

        heart_image = pygame.image.load('img/heart.png').convert_alpha()
        heart_width = heart_image.get_width()
        heart_spacing = 10
        number_of_hearts = 3 - self.__missed_orders

        total_hearts_width = heart_width * number_of_hearts + heart_spacing * (number_of_hearts - 1)
        start_x = (self.__screen.get_width() - total_hearts_width) / 2

        for i in range(number_of_hearts):
            self.__screen.blit(heart_image, (start_x + i * (heart_width + heart_spacing), 35))



    def __show_fps(self) -> None:
        """ Affiche le nombre de trames par seconde (FPS). """
        info = f"{round(self.__clock.get_fps())} FPS"
        text_surface = self.__font.render(info, True, (255, 255, 255))
        pos = self.__screen.get_width() - text_surface.get_width() - 10, 10
        self.__screen.blit(text_surface, pos)

    def __show_game_over_screen(self):
        """ Affiche l'écran de fin de jeu et attend un moment avant de continuer. """

        game_over_image = pygame.image.load('img/gameover.png').convert_alpha()
        game_over_settings = pygame.transform.scale(game_over_image, (self.__screen.get_width(), self.__screen.get_height()))
        self.__screen.blit(game_over_settings, (0, 0))
        pygame.display.flip()
        pygame.time.wait(settings.IMAGES_TRANSITION_TIME_MS)

    def __reset_game(self):
        """ Réinitialise le jeu pour un nouveau départ. """

        for grill in self.__grills:
            grill.reset()
        for fryer in self.__fryers:
            fryer.reset()
        for filling_station in self.__filling_stations:
            filling_station.reset()
        for assembly_station in self.__assembly_stations:
            assembly_station.reset()
        for cutting_station in self.__cutting_stations:
            cutting_station.reset()
        for platter in self.__platters:
            platter.reset()

        self.__order_board.reset()
        orders.spawner.reset()


        initial_position_chef_one = (self.__screen.get_width() * (1.9/4), self.__screen.get_height() * (2/4))
        initial_position_chef_two = (self.__screen.get_width() * (2.1/4), self.__screen.get_height() * (2/4))
        self.__chef_one.reset(initial_position_chef_one)
        self.__chef_two.reset(initial_position_chef_two)

        self.total_tips = 0
        self.__missed_orders = 0


    def user_requested_quit(self):
        return not self.__running

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
        if self.__chef.food:
            if grill.start_cooking(self.__chef.food):
                self.__chef.drop_food()
        else:
            if grill.has_cooked_patty():
                cooked_patty = grill.get_cooked_patty()
                if cooked_patty:
                    self.__chef.grab_food(cooked_patty)
            elif grill.has_overcooked_or_burnt_patty():
                burnt_patty = grill.get_overcooked_or_burnt_patty()
                if burnt_patty:
                    self.__chef.grab_food(burnt_patty)
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
        delivered_order = self.__chef.deliver_meal(orderboard)
        if delivered_order:
            tip = delivered_order.calculate_tip()
            self.total_tips += tip
            orders.spawner.increase_acceleration(1.2)  # Augmenter de 20%

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

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP]:
                self.__chef = self.__chef_one
            elif event.key in [pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_w]:
                self.__chef = self.__chef_two

            if event.key == pygame.K_SPACE:
                self.handle_space_key()

            chef, direction = self.__chef_controls.get(event.key, (None, None))
            if chef:
                self.__update_chef_movement(chef, direction, True)

        elif event.type == pygame.KEYUP:
            chef, direction = self.__chef_controls.get(event.key, (None, None))
            if chef:
                self.__update_chef_movement(chef, direction, False)

    def __update_chef_movement(self, chef, direction, is_moving):

        if direction == 'left':
            chef.is_moving_left = is_moving
            chef.move_horizontal(-1 if is_moving else 0)
        elif direction == 'right':
            chef.is_moving_right = is_moving
            chef.move_horizontal(1 if is_moving else 0)
        elif direction == 'up':
            chef.is_moving_up = is_moving
            chef.move_vertical(-1 if is_moving else 0)
        elif direction == 'down':
            chef.is_moving_down = is_moving
            chef.move_vertical(1 if is_moving else 0)

    
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
