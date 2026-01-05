"""Module contenant les classes Player et Status."""

from item import Inventory
from item import Item
from quests import QuestManager

class Status:
    """
    Classe représentant les statistiques et récompenses d'un joueur.

    Attributes:
        max_weight (float): Le poids maximum que le joueur peut porter.
        move_count (int): Le nombre de déplacements effectués par le joueur.
        rewards (list[str]): La liste des récompenses obtenues par le joueur.

    Methods:
        add_reward(self, reward): Ajoute une récompense au joueur.
        show_rewards(self): Affiche les récompenses obtenues.
    """
    def __init__(self, max_weight=10):
        self.max_weight = max_weight
        self.move_count = 0
        self.rewards = []

    def add_reward(self, reward):
        """
        Ajoute une récompense au joueur.

        Args:
            reward (str): La récompense à ajouter.
        """
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            print(f"\n🎁 Vous avez obtenu : {reward}\n")

    def show_rewards(self):
        """
        Affiche toutes les récompenses obtenues par le joueur.
        """
        if not self.rewards:
            print("\n🎁 Aucune récompense obtenue pour le moment.\n")
        else:
            print("\n🎁 Vos récompenses :")
            for reward in self.rewards:
                print(f"  • {reward}")
            print()


class Player:
    """
    Classe représentant un joueur dans le jeu.

    Attributes:
        name (str): Le nom du joueur.
        current_room (Room | None): La salle actuelle du joueur.
        history (list[Room]): L'historique des salles visitées.
        inventory (Inventory): L'inventaire du joueur.
        quest_manager (QuestManager): Le gestionnaire de quêtes du joueur.
        status (Status): Les statistiques et récompenses du joueur.

    Methods:
        get_total_weight(self): Retourne le poids total des objets portés.
        move(self, direction): Déplace le joueur vers une salle voisine.
        get_history(self): Retourne l'historique des salles visitées.
        get_inventory(self): Retourne la description de l'inventaire.
    """

    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = Inventory()
        self.quest_manager = QuestManager()
        self.status = Status()
        self.quest_manager = QuestManager(self)
        self.rewards = []

    def get_total_weight(self):
        """
        Calcule le poids total des objets dans l'inventaire.

        Returns:
            float: Le poids total des objets.
        """
        return sum(item.weight for item in self.inventory.items)

    def add_reward(self, reward):
        if reward == "un cookie":
            cookie = Item(
                name="cookie",
                description="Un délicieux cookie offert par Manon",
                weight=0.2
            )
            self.inventory.add_item(cookie)
            print("🍪 Vous recevez un cookie !")


    def get_history(self):
        """
        Retourne l'historique des salles visitées par le joueur.

        Returns:
            str: Une description textuelle des salles visitées.
        """
        if len(self.history) <= 1:
            return ""
        text = "\nVous avez déjà visité les pièces suivantes :\n"
        for room in self.history[:-1]:
            text += f"    - {room.description}\n"
        return text

    def get_inventory(self):
        """
        Retourne une description textuelle de l'inventaire du joueur.

        Returns:
            str: La description des objets présents dans l'inventaire.
        """
        return self.inventory.get_inventory()
