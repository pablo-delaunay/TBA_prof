"""Ce module contient les classes Item et Inventory."""
class Item:
    """
    Cette classe représente un objet (item) du jeu.

    Attributes:
        name (str): Le nom de l'objet.
        description (str): La description de l'objet.
        weight (float): Le poids de l'objet en kilogrammes.

    Methods:
        __init__(self, name, description, weight): Constructeur de l'objet.
        __str__(self): Représentation en chaîne de caractères de l'objet.
    """
    def __init__(self,name, description, weight, price=0):
        self.name = name
        self.description = description
        self.weight = weight
        self.price = price


    def __str__(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"


    def get_weight(self):
        """Retourne le poids de l'objet."""
        return self.weight

    def get_description(self):
        """Retourne la description de l'objet."""
        return self.description

class Inventory:
    """
    Cette classe représente un inventaire d'objets. 
    Un inventaire peut contenir plusieurs objets et permet de les gérer.

    Attributes:
        items (list[Item]): La liste des objets contenus dans l'inventaire.

    Methods:
        __init__(self): Constructeur de l'inventaire.
        add_item(self, item): Ajoute un objet à l'inventaire.
        remove_item(self, item_name): Retire un objet par son nom et le retourne.
        has_item(self, item_name): Vérifie si un objet avec ce nom est présent.
        get_inventory(self, prefix_message="Vous disposez des items suivants :"):
        Retourne une description de l'inventaire.
    """
    def __init__(self):
        self.items = []

    def add_item(self, item):
        """Ajoute un objet à l'inventaire.

        Args:
            item (Item): L'objet à ajouter.
        """
        self.items.append(item)

    def remove_item(self, item_name):
        """Retire un objet de l'inventaire par son nom.

        Args:
            item_name (str): Le nom de l'objet à retirer.

        Returns:
            Item: L'objet retiré s'il existe, sinon None.
        """
        for i, item in enumerate(self.items):
            if item.name.lower() == item_name.lower():
                return self.items.pop(i)
        return None

    def has_item(self, item_name):
        """
        Vérifie si l'inventaire contient un objet avec ce nom.

        Args:
            item_name (str): Le nom de l'objet à chercher.

        Returns:
            bool: True si l'objet est présent, False sinon.
        """
        return any(item.name.lower() == item_name.lower() for item in self.items)



    def get_inventory(self, prefix_message="Vous disposez des items suivants :"):
        """
        Retourne une description textuelle de l'inventaire.

        Args:
            prefix_message (str, optional): Le message à afficher avant la liste des items.
            Par défaut "Vous disposez des items suivants :".

        Returns:
            str: La description complète de l'inventaire.
        """
        if not self.items:
            if prefix_message.startswith('La pièce'):
                return "Il n'y a rien ici."
            return "Vous ne disposez d'aucun item."

        inv = f"{prefix_message}\n"
        for item in self.items:
            inv += f" - {item}\n"
        return inv

    def get_item(self, item_name):
        """
        Retourne un objet sans le retirer de l'inventaire.
        """
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        return None
