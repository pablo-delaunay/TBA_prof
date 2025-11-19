# Define the Player class.
class Player():

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

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
        print(self.current_room.get_long_description())
        return True

    