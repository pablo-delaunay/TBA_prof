"""
Module character.

Contient la classe Character représentant un personnage non-joueur (PNJ)
dans le jeu, avec ses messages et son déplacement aléatoire.
"""
import random
from item import Inventory

class Character:
    """
    Cette classe représente un personnage non-joueur (PNJ) dans le jeu.
    """

    # pylint: disable=too-many-instance-attributes
    # Note: Si vous ajoutez encore des attributs,
    # envisagez de regrouper (ex: name et description dans une dataclass).

    def __init__(self, name, description, **kwargs):
        """
        Initialise un personnage.
        Args:
            name (str): Nom du personnage.
            description (str): Description du personnage.
            **kwargs: current_room, msgs, inventory.
        """
        self.name = name
        self.description = description
        self.current_room = kwargs.get('current_room')
        self.msgs = kwargs.get('msgs', [])
        self._msg_index = 0
        self.last_room = self.current_room
        self.inventory = kwargs.get('inventory') or Inventory()


    def __str__(self):
        """Retourne une représentation lisible du personnage."""
        return f"{self.name} : {self.description}"

    def receive_item(self, item):
        """Ajoute un objet à l'inventaire du personnage."""
        self.inventory.add_item(item)
        print(f"{self.name} a reçu '{item.name}'.")

    def get_msg(self):
        """
        Affiche un message du personnage.

        Le message est affiché et remis à la fin de la liste pour permettre un cycle.
        Si le personnage n'a aucun message, un avertissement est affiché.
        """
        if not self.msgs:
            print(f"{self.name} n'a rien à dire pour l'instant.")
            return

        message = self.msgs.pop(0)
        print(message)
        self.msgs.append(message)

    def move(self):
        """
        Déplace le personnage aléatoirement vers une salle voisine.
        
        Returns:
            tuple: (bool, Room) True si déplacé, et l'ancienne salle.
        """
        if random.random() < 0.5 or not self.current_room:
            return False, self.current_room

        exits = []
        for exit_info in self.current_room.exits.values():
            if exit_info is None:
                continue

            # Gestion des portes verrouillées
            if isinstance(exit_info, tuple):
                room, door = exit_info
                if not door.locked:
                    exits.append(room)
            else:
                exits.append(exit_info)

        if not exits:
            return False, self.current_room

        old_room = self.current_room
        new_room = random.choice(exits)

        # Mise à jour des listes de personnages dans les salles
        if self in old_room.characters:
            old_room.characters.remove(self)

        new_room.characters.append(self)
        self.current_room = new_room

        return True, old_room
