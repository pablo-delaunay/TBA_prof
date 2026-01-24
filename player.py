"""Module contenant les classes Player et Status."""

from item import Inventory
from item import Item
from quests import QuestManager

class Status:
    """
    Classe représentant les statistiques, l'argent et récompenses d'un joueur.
    """
    def __init__(self, max_weight=10):
        self.max_weight = max_weight
        self.move_count = 0
        self.rewards = []
        self.money = 0  # L'argent est maintenant géré ici

    def add_reward(self, reward):
        """Ajoute une récompense au joueur."""
        if reward and reward not in self.rewards:
            self.rewards.append(reward)

    def show_rewards(self):
        """Affiche toutes les récompenses obtenues par le joueur."""
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
    """

    def __init__(self, name):
        """Initialise un joueur avec ses composants."""
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = Inventory()
        self.status = Status()
        self.quest_manager = QuestManager(self)
        # On ne définit plus money et rewards ici pour rester sous la limite Pylint

    def get_total_weight(self):
        """Calcule le poids total des objets dans l'inventaire."""
        return sum(item.weight for item in self.inventory.items)

    def add_reward(self, reward):
        """Ajoute une récompense et gère les cas particuliers comme le cookie."""
        if reward == "un cookie":
            cookie = Item(
                name="cookie",
                description="Un délicieux cookie offert par Manon",
                weight=0.2
            )
            self.inventory.add_item(cookie)
            print("🍪 Vous recevez un cookie !")

        # On délègue le stockage du texte de récompense à status
        self.status.add_reward(reward)

    def get_history(self):
        """Retourne l'historique des salles visitées par le joueur."""
        if len(self.history) <= 1:
            return ""
        text = "\nVous avez déjà visité les pièces suivantes :\n"
        for room in self.history[:-1]:
            text += f"    - {room.name}\n"
        return text

    def get_inventory(self):
        """Retourne une description textuelle de l'inventaire du joueur."""
        return self.inventory.get_inventory()

    def add_money(self, amount):
        """Ajoute une somme d'argent au statut du joueur."""
        self.status.money += amount
        print(f"💰 Vous gagnez {amount}€")

    def spend_money(self, amount):
        """
        Débite l'argent du joueur s'il en a assez.
        Returns: bool: True si la transaction a réussi.
        """
        if self.status.money < amount:
            print("❌ Vous n'avez pas assez d'argent.")
            return False
        self.status.money -= amount
        print(f"💸 Vous dépensez {amount}€")
        return True

    def show_money(self):
        """Affiche le solde actuel du joueur."""
        print(f"💰 Argent : {self.status.money}€")
