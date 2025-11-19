# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction (N, E, S, O, U, D)", Actions.go, 1)
        self.commands["go"] = go
        
        # Setup rooms

        
        Esiee = Room("Esiee", "Lisa est dans la rue de l'esiee, au milieu des étudiants ")
        self.rooms.append(Esiee)
        Bu = Room("Bu", " Lisa est dans la bibliotèque de l'école et vous apercevez Berko au loin")
        self.rooms.append(Bu)
        Rue = Room("Rue", "Vous êtes dans la rue, de l'air frais enfin")
        self.rooms.append(Rue)
        Magasin = Room("Magasin", "Lisa est dans un magasin, il y a tout le nécessaire pour une CE (résistances et goûts).")
        self.rooms.append(Magasin)
        ChezAmine = Room("Chez Amine", "Lisa est rentré chez Amine")
        self.rooms.append(ChezAmine)
        Couloir = Room("Couloir", "Lisa est devant la porte de chez Amine")
        self.rooms.append(Couloir)
        Crackheads = Room("Crackheads", "Lisa croise des crackheads et se fait planter (29/09/2005 - 21/01/2026)")
        self.rooms.append(Crackheads)
        Ascenseur2 = Room("Ascenseur2", "Lisa est dans l'ascenseur, au deuxième étage du crous Monstesquieu")
        self.rooms.append(Ascenseur2)
        Ascenseur1 = Room("Ascenseur1", "Lisa est dans l'ascenseur, au premier étage du crous Monstesquieu")
        self.rooms.append(Ascenseur1)
        SaadJunior = Room("SaadJunior", "Lisa croise saad dans la Junior Entreprise il lui tend ses clés")
        self.rooms.append(SaadJunior)
        # Create exits for rooms

        Esiee.exits = {"N" : SaadJunior, "E" : None, "S" : Rue, "O" : Bu, "U" : None, "D" : None}
        Bu.exits = {"N" : None, "E" : Esiee, "S" : None, "O" : None,"U" : None, "D" : None}
        Rue.exits = {"N" : None, "E" : ChezAmine, "S" : Magasin, "O" : Crackheads,"U" : None, "D" : None}
        Magasin.exits = {"N" : Rue, "E" : None, "S" : None, "O" : None,"U" : None, "D" : None}
        ChezAmine.exits = {"N" : None, "E" : None, "S" : Couloir, "O" : None,"U" : None, "D" : None}
        Couloir.exits = {"N" : ChezAmine, "E" : None, "S" : Ascenseur2, "O" : None,"U" : None, "D" : None}
        Ascenseur1.exits = {"N" : None, "E" : None, "S" : None, "O" : Rue,"U" : Ascenseur2, "D" : None}
        Ascenseur2.exits = {"N" : Couloir, "E" : None, "S" : None, "O" : None,"U" : None, "D" : Ascenseur1}
        SaadJunior.exits = {"N" : None, "E" : None, "S" : Esiee, "O" : None,"U" : None, "D" : None}

        Esiee.fail_messages = {
            "E": "Il y a un mur",
            "U": "Tu veux t'envoler ? Il y a un plafond", 
            "D": "Il n'y a pas de tunnel sous terrain désolé",
        }
        SaadJunior.fail_messages = {
            "E": "Il y a un mur", 
            "O": "Il y a un mur", 
            "N": "Il y a Yann avec un poème à la main, Lisa fait demi-tour et reste avec Saad.",
            "U": "Tu veux t'envoler ? Il y a un plafond",
            "D": "Il n'y a pas de tunnel sous terrain désolé",
        }
        Bu.fail_messages = {
            "U": "Tu veux t'envoler ?", 
            "D": "Il n'y a pas de tunnel sous terrain désolé", 
        }
        Magasin.fail_messages = {
            "U": "Tu veux t'envoler ?", 
            "D": "Il n'y a pas de tunnel sous terrain désolé", 
        }
        Rue.fail_messages = {
            "U": "Tu veux t'envoler ?", 
            "D": "Il n'y a pas de tunnel sous terrain désolé",
            "N": "Tu n'as pas ta carte étudiante donc ne peut plus rentrer" 
        }
        Couloir.fail_messages = {
            "U": "Tu veux t'envoler ? Il y a un plafond", 
            "D": "Il n'y a pas de tunnel sous terrain désolé", 
        }
        ChezAmine.fail_messages = {
            "U": "Tu veux t'envoler ? Il y a un plafond", 
            "D": "Il n'y a pas de tunnel sous terrain désolé", 
        }


        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = Esiee

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"  ")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\n Bienvenue {self.player.name}, vous incarnez Lisa une jeune étudiante de l'Esiee à la recherche d'une CE. Elle est en total manque de nicotines, vous devez absolument l'aider à en trouver une. Bon courage, kiffez, croquez la vie à pleine dents, fumez avant que la vie vous fume. \n")
        print("Entrez 'help' si vous avez besoin d'aide. \n")
        #
        print(self.player.current_room.get_long_description())

    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
