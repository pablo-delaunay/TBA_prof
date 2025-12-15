# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from item import Inventory
from room import Door
from character import Character

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
        back_cmd = Command("back", " : revenir à la pièce précédente", Actions.back, 0)
        self.commands["back"] = back_cmd
        look_command = Command("look", " : observer la pièce et voir les objets présents", Actions.look, 0)
        self.commands["look"] = look_command
        take_cmd = Command("take", " <item> : prendre un objet", Actions.take, 1)
        self.commands["take"] = take_cmd
        drop_cmd = Command("drop", " <item> : déposer un objet", Actions.drop, 1)
        self.commands["drop"] = drop_cmd
        check_cmd = Command("check", " : afficher l'inventaire", Actions.check, 0)
        self.commands["check"] = check_cmd
        unlock_command = Command("unlock", " <direction> : déverrouiller une porte avec la clé correspondante", Actions.unlock, 1)
        self.commands["unlock"] = unlock_command
        talk_cmd = Command("talk", " <someone> : parler à un personnage", Actions.talk, 1)
        self.commands["talk"] = talk_cmd


        # Setup rooms

        
        Esiee = Room("Esiee", "Lisa est dans la rue de l'esiee, au milieu des étudiants ")
        self.rooms.append(Esiee)
        Bu = Room("Bu", " Lisa est dans la bibliotèque de l'école et vous apercevez Berko au loin")
        self.rooms.append(Bu)
        Rue = Room("Rue", "Lisa est dans la rue, de l'air frais enfin")
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
        Ascenseur1 = Room("Ascenseur1", "Lisa est dans l'ascenseur, au premier étage du crous Monstesquieu (Amine vie ici)")
        self.rooms.append(Ascenseur1)
        SaadJunior = Room("SaadJunior", "Lisa croise saad dans la Junior Entreprise il lui tend ses clés")
        self.rooms.append(SaadJunior)
        # Create exits for rooms

        self.characters = []
        Saad = Character("Saad", "un ami", SaadJunior, ["slt lisa c'est saad"])
        Amine = Character("Amine", "un ami", ChezAmine, ["slt lisa c'est amine"])
        Berko = Character("Berko", "un ami", Bu, ["slt lisa c'est berko"])

        self.characters.extend([Saad, Amine, Berko])
        
        SaadJunior.characters.append(Saad)
        ChezAmine.characters.append(Amine)
        Bu.characters.append(Berko)

       


    

        


        Esiee.exits = {"N" : SaadJunior, "E" : None, "S" : Rue, "O" : Bu, "U" : None, "D" : None}
        Bu.exits = {"N" : None, "E" : Esiee, "S" : None, "O" : None,"U" : None, "D" : None}
        Rue.exits = {"N" : (Esiee, Door(locked=True, key_name="carte")), "E" : Ascenseur1, "S" : Magasin, "O" : Crackheads,"U" : None, "D" : None}
        Magasin.exits = {"N" : Rue, "E" : None, "S" : None, "O" : None,"U" : None, "D" : None}
        ChezAmine.exits = {"N" : None, "E" : None, "S" : Couloir, "O" : None,"U" : None, "D" : None}
        Couloir.exits = {"N" :  (ChezAmine, Door(locked=True, key_name="clé")), "E" : None, "S" : Ascenseur2, "O" : None,"U" : None, "D" : None}
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


        clés = Item("clés", "celles de chez Amine",0.001)
        SaadJunior.items = ["clés"]
        carte = Item("carte", "C'est ta carte étudiante elle te permet de rentrer dans l'école",0.001)
        Magasin.items = ["carte"]

        # Porte verrouillée pour entrer chez Amine
        porte_chez_amine = Door(locked=True, key_name="clés")
        # On remplace l'exit normale par un tuple (room, door)
        Couloir.exits["N"] = (ChezAmine, porte_chez_amine)
        porte_Esiee = Door(locked=True, key_name="carte")
        Rue.exits["N"] = (Esiee, porte_Esiee)


        # Ajouter les items à certaines salles
        SaadJunior.inventory.add_item(clés)
        Magasin.inventory.add_item(carte)


        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = Esiee
        self.player.history.append(self.player.current_room)


    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()

        while not self.finished:
            self.process_command(input("> "))




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

    def back(game, list_of_words, number_of_parameters):
        if len(game.player.history) <= 1:
            print("\nVous ne pouvez pas revenir en arrière.\n")
            return

        # Supprime la salle actuelle de l'historique
        game.player.history.pop()

        # Revenir à la salle précédente
        game.player.current_room = game.player.history[-1]

        # Afficher la description et l'historique
        print(game.player.current_room.get_long_description())
        hist = game.player.get_history()
        if hist != "":
            print(hist)

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
