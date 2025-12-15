# Define the Player class.
from item import Inventory
from quests import QuestManager
from quests import Quest

class Player():

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = Inventory()
        self.max_weight = 10
        self.quest_manager = QuestManager()
        self.rewards = []
        self.move_count = 0

    def get_total_weight(self):
        return sum(item.weight for item in self.inventory.items)

        
            # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits.get(direction)

        if next_room is None:

            # Vérifie s'il existe un message personnalisé dans la room
            if direction in self.current_room.fail_messages:
                print("\n" + self.current_room.fail_messages[direction] + "\n")
            else:
                # message standard si aucun message personnalisé n'existe
                print("\nImpossible d'aller dans cette direction.\n")

            return False

        
        # Set the current room to the next room.
        self.current_room = next_room
        self.history.append(self.current_room)
        print(self.current_room.get_long_description())

        hist = self.get_history()
        if hist != "":
            print(hist)
        return True

    def get_history(self):
        if len(self.history) <= 1:
            return ""  

        text = "\nVous avez déja visité les pièces suivantes:\n"
        for room in self.history[:-1]:  
            text += f"    - {room.description}\n"
        return text

    def get_inventory(self):
        if not self.inventory:
            return "Vous ne disposez d'aucun item."
            inv = "Vous disposez des items suivants :\n"
            for item in self.inventory:
                inv += f" - {item}\n"
            return inv
        

    def add_reward(self, reward):
        """
        Add a reward to the player's rewards list.
        
        Args:
            reward (str): The reward to add.
            
        Examples:
        
        >>> player = Player("Bob")
        >>> player.add_reward("Épée magique") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Épée magique
        <BLANKLINE>
        >>> "Épée magique" in player.rewards
        True
        >>> player.add_reward("Épée magique") # Adding same reward again
        >>> len(player.rewards)
        1
        """
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            print(f"\n🎁 Vous avez obtenu: {reward}\n")


    def show_rewards(self):
        """
        Display all rewards earned by the player.
        
        Examples:
        
        >>> player = Player("Charlie")
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        >>> player.add_reward("Bouclier d'or") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Bouclier d'or
        <BLANKLINE>
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vos récompenses:
        • Bouclier d'or
        <BLANKLINE>
        """
        if not self.rewards:
            print("\n🎁 Aucune récompense obtenue pour le moment.\n")
        else:
            print("\n🎁 Vos récompenses:")
            for reward in self.rewards:
                print(f"  • {reward}")
            print()