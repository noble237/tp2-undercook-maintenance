import random
import time

from queue import Queue
from threading import Thread, Event

from beverage import Beverage
from burger import Burger
from fries import Fries
from meal import Meal


ORDER_TICK = 0.20  # en secondes


class Order(Thread):
    """
    Commande. Une commande contient un hambourgeois et peut-être une boisson et peut-être un cornet de frites.
    Chaque commande doit être préparée et livrée dans un temps aléatoire déterminé au moment de sa création.
    """

    __MIN_EXPIRATION_TIME = 60.0  # en secondes
    __MAX_EXPIRATION_TIME = 240.0  # en secondes

    def __init__(self, order_id: int) -> None:
        """
        Initialise la commande.
        :param order_id: identifiant de la commande (unique et créé par le générateur de commandes)
        """
        super().__init__()

        self.__order_id = order_id

        self.__meal = Meal()
        burger = Burger.random()
        if burger:
            self.__meal.add_burger(burger)
        beverage = Beverage.random()
        if beverage:
            self.__meal.add_beverage(beverage)
        fries = Fries.random()
        if fries:
            self.__meal.add_fries(fries)

        self.__expiration_time = random.uniform(Order.__MIN_EXPIRATION_TIME, Order.__MAX_EXPIRATION_TIME)
        self.__remaining_time = self.__expiration_time

        self.__event = Event()  # événement servant à arrêter la tâche (va aussi la réveiller si nécessaire)

    def run(self) -> None:
        """ Méthode principale exécutée par la tâche de commande. """
        previous_time = time.time()

        while not self.__event.is_set():
            now = time.time()
            self.__remaining_time = max(0, self.__remaining_time - (now - previous_time))
            previous_time = now
            self.__event.wait(ORDER_TICK)

    def stop(self) -> None:
        """ Arrête la tâche de commande. """
        self.__event.set()

    def get_remaining_time_percentage(self) -> float:
        """
        Récupère le temps qui reste pour compléter la commande (en pourcentage).
        :return: pourcentage du temps restant (de 0.0 à 100.0)
        """
        return self.__remaining_time / self.__expiration_time * 100.0

    def has_expired(self) -> bool:
        return self.__remaining_time == 0

    def calculate_tip(self) -> float:
        base_tip = 1
        item_bonus = 2

        items_count = 0
        if self.meal.burger is not None:
            items_count += 1
        if self.meal.beverage is not None:
            items_count += 1
        if self.meal.fries is not None:
            items_count += 1

        if items_count == 0:
            return base_tip

        time_bonus = self.get_remaining_time_percentage() / (10 * items_count)

        tip = base_tip + items_count * item_bonus + time_bonus
        return round(tip, 2)

    @property
    def meal(self) -> Meal:
        return self.__meal

    @property
    def beverage(self) -> Beverage or None:
        return self.__meal.beverage

    @property
    def burger(self) -> Burger or None:
        return self.__meal.burger

    @property
    def fries(self) -> Fries or None:
        return self.__meal.fries

    @property
    def order_id(self) -> int:
        return self.__order_id


class __OrderSpawner(Thread):
    """
    Générateur de commandes.
    """
    __DEFAULT_MIN_TIME_BETWEEN_ORDERS = 20  # en secondes
    __DEFAULT_MAX_TIME_BETWEEN_ORDERS = 45  # en secondes

    __TIME_BEFORE_FIRST_ORDER = 2  # en secondes

    __next_order_id = 1

    def __init__(self) -> None:
        super().__init__()

        self.__queue = Queue()  # queue dans laquelle on place les commandes générées
        self.__event = Event()  # événement servant à arrêter la tâche (va aussi la réveiller si nécessaire)

        self.__min_time_between = self.__DEFAULT_MIN_TIME_BETWEEN_ORDERS
        self.__max_time_between = self.__DEFAULT_MAX_TIME_BETWEEN_ORDERS

        self.__acceleration_factor = 1.0
        self.__creating_orders = True  # va créer des incidents seulement si __creating_incidents est True

    def run(self) -> None:
        """ Méthode principale exécutée par la tâche du générateur de commandes. """
        # attendre un certain temps avant de générer la première commande
        self.__create_and_send_next_order(self.__TIME_BEFORE_FIRST_ORDER, self.__TIME_BEFORE_FIRST_ORDER + 2)

        # tant que la tâche exécute, on génère des commandes
        while not self.__event.is_set():
            self.__create_and_send_next_order(self.__min_time_between, self.__max_time_between)

    def pause(self) -> None:
        """ Pause la génération de commandes. """
        self.__creating_orders = False

    def unpause(self) -> None:
        """ Relance la génération de commandes. """
        self.__creating_orders = True

    def stop(self) -> None:
        """ Arrête le générateur de commandes. """
        self.__event.set()

    def get(self) -> list:
        """
        Récupère toutes les commandes se trouvant dans la queue de commandes.
        :return: liste contenant les commandes récupérées
        """
        orders = []

        if not self.__event.is_set():
            while not self.__queue.empty():
                orders.append(self.__queue.get())

        return orders

    def put(self, order: Order) -> None:
        """
        Place une commande dans la queue de commandes.
        :param order: commande à placer dans la queue
        :return: aucun
        """
        if not self.__event.is_set():
            self.__queue.put(order)


    def __create_and_send_next_order(self, min_delay: int, max_delay: int) -> None:
        """
        Crée et envoie la prochaine commande.
        :param min_delay: délai minimum à respecter avant de créer la commande
        :param max_delay: délai maximal pour créer la commande
        :return: aucun
        """

        time_to_order = random.uniform(min_delay, max_delay) / self.__acceleration_factor
        self.__event.wait(time_to_order)

        if self.__creating_orders:
            self.__queue.put(Order(self.__next_order_id))
            self.__next_order_id += 1

    def increase_acceleration(self, increment: float) -> None:
        self.__acceleration_factor *= increment

    def reset(self):
        self.__acceleration_factor = 1.0

# générateur de commandes (singleton implémenté avec un Global Object Pattern de python)
spawner = None


def init() -> None:
    """ Initialise le spawner, mais ne le démarre pas. """

    global spawner
    if not spawner:
        spawner = __OrderSpawner()
