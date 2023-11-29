import pygame

from orders import Order
from order_sprite import OrderSprite


class OrderBoard:
    """
    Tableau d'affichage des commandes en attente.
    """

    __LEFT_OFFSET = 10  # distance (en pixels) du bord gauche de l'écran où commencer l'affichage des commandes
    __SPACING = 70  # espacement (en pixels) entre chaques coins supérieurs gauches des commandes affichées

    def __init__(self) -> None:

        self.__left_pos = OrderBoard.__LEFT_OFFSET

        self.__waiting_orders_sprite_group = pygame.sprite.Group()
        self.__waiting_orders = []

    def __del__(self) -> None:
        """
        Destructeur : arrête les tâches associées aux commandes et détruit les sprites.
        :return: aucun
        """
        for order, order_sprite in self.__waiting_orders:
            order.stop()
            order_sprite.kill()

    def add_orders(self, orders: list) -> None:
        """
        Ajoute des commandes au tableau d'affichage.
        :param orders: liste de commandes à ajouter
        :return:
        """
        for order in orders:
            order_sprite = OrderSprite(order)
            order_sprite.push_to(self.__left_pos)
            self.__left_pos += OrderBoard.__SPACING

            self.__waiting_orders_sprite_group.add(order_sprite)
            self.__waiting_orders.append((order, order_sprite))

        self.__pack()

    def collides_with(self, sprite: pygame.sprite.Sprite) -> Order or None:
        """
        Retourne la commande avec laquelle un sprite est en contact.
        :param sprite: sprite avec lequel on veut vérifier s'il y a collision
        :return: commande en contact s'il y a collision, None sinon
        """
        if order_sprite := pygame.sprite.spritecollideany(sprite, self.__waiting_orders_sprite_group):
            return order_sprite.order

        return None

    def draw(self, surface: pygame.Surface) -> None:
        """
        Dessine toutes les commandes du tableau d'affichage.
        :param surface: surface sur laquelle dessiner le tableau
        :return: aucun
        """
        self.__waiting_orders_sprite_group.draw(surface)

    def remove_order(self, order_id: int) -> None:
        """
        Retire une commande du tableau d'affichage. On retire une commande lorsqu'elle est complétée ou expirée.
        :param order_id: identifiant unique de la commande à retirer
        :return: aucun
        """
        for i, waiting_order in enumerate(self.__waiting_orders):
            order, order_sprite = waiting_order
            if order.order_id == order_id:
                order.stop()
                order_sprite.kill()
                del self.__waiting_orders[i]
                break
                
        self.__pack()

    def update(self) -> None:
        """
        Met à jour le tableau d'affichage : retire les commandes expirées et
        met à jour l'affichage des commandes en attente.
        :return: aucun
        """
        # retirer les commandes expirées
        for order, _ in self.__waiting_orders:
            if order.has_expired():
                self.remove_order(order.order_id)

        # mettre à jour tous les sprites
        for _, order_sprite in self.__waiting_orders:
            order_sprite.update()

    def __pack(self) -> None:
        """
        Pousse les commandes en attentes vers la gauche, comble les espaces vides au besoin.
        :return: aucun
        """
        left_align = OrderBoard.__LEFT_OFFSET
        for waiting_order in self.__waiting_orders:
            waiting_order[1].push_to(left_align)
            left_align += OrderBoard.__SPACING
