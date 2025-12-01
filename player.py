# Define the Player class.
from item import Inventory

class Player():

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = Inventory()
        self.max_weight = 10

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