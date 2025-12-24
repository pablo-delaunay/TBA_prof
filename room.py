"""Module contenant les classes Room et Door."""

from item import Inventory

class Room:
    """
    Cette classe représente une salle dans le jeu.

    Attributes:
        name (str): Le nom de la salle.
        description (str): La description de la salle.
        exits (dict): Dictionnaire des sorties, avec la direction comme clé et
                      la salle (ou tuple salle+porte) comme valeur.
        fail_messages (dict): Messages personnalisés lorsqu'un déplacement échoue.
        inventory (Inventory): L'inventaire de la salle.
        items (list[Item]): Liste des objets présents dans la salle.
        characters (list[Character]): Liste des personnages présents dans la salle.

    Methods:
        get_exit(self, direction): Retourne la salle (ou tuple) correspondant à la direction.
        get_exit_string(self): Retourne une chaîne listant toutes les sorties disponibles.
        get_long_description(self): Retourne la description complète de la salle.
        get_inventory(self): Retourne la description de l'inventaire et des personnages présents.
    """

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.fail_messages = {}
        self.inventory = Inventory()
        self.items = []
        self.characters = []

    def get_exit(self, direction):
        """
        Retourne la salle ou le tuple (salle, porte) correspondant à la direction.

        Args:
            direction (str): La direction souhaitée (ex: 'N', 'E', ...).

        Returns:
            Room | tuple | None: La salle ou le tuple (salle, porte)
            si la sortie existe, sinon None.
        """
        return self.exits.get(direction, None)

    def get_exit_string(self):
        """
        Retourne une chaîne décrivant les sorties disponibles de la salle.

        Returns:
            str: Une chaîne listant toutes les sorties (ex: "Sorties: N, E, S").
        """
        exit_string = "Sorties: "
        for sortie in self.exits:
            if self.exits.get(sortie) is not None:
                exit_string += sortie + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    def get_long_description(self):
        """
        Retourne la description complète de la salle, incluant les sorties.

        Returns:
            str: Description longue de la salle.
        """
        return f"\n{self.description}\n\n{self.get_exit_string()}\n"

    def get_inventory(self):
        """
        Retourne une description textuelle de l'inventaire de la salle et des personnages présents.

        Returns:
            str: Description des objets et personnages présents dans la salle.
        """
        inv_text = self.inventory.get_inventory(prefix_message="La pièce contient :")

        if self.characters:
            inv_text += "\nPersonnages présents :\n"
            for char in self.characters:
                inv_text += f" - {char.name}\n"
        else:
            inv_text += "\nPersonne n'est ici.\n"

        return inv_text


class Door:
    """
    Cette classe représente une porte entre deux salles.

    Attributes:
        locked (bool): True si la porte est verrouillée, False sinon.
        key_name (str | None): Nom de l'objet clé nécessaire pour déverrouiller la porte.

    Methods:
        __init__(self, locked=True, key_name=None): Constructeur de la porte.
    """

    def __init__(self, locked=True, key_name=None):
        self.locked = locked
        self.key_name = key_name

    def unlock(self, key_name):
        """
        Déverrouille la porte si la clé correspond.

        Args:
            key_name (str): Le nom de la clé utilisée pour déverrouiller la porte.

        Returns:
            bool: True si la porte a été déverrouillée, False sinon.
        """
        if self.locked and self.key_name == key_name:
            self.locked = False
            return True
        return False

    def is_locked(self):
        """ Retourne l'état de la porte."""
        return self.locked
