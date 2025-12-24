" Main game class"
from room import Room
from room import Door
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from quests import Quest

class Game:
    """Main game class."""
    def __init__(self):
        """Initialize the game state."""
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.rooms = {}
        self.player = None
        self.characters = []

    def setup(self):
        """Set up the game."""
        self.setup_commands()
        self.setup_rooms()
        self.setup_fail_messages()
        self.setup_characters()
        self.setup_items()

    def setup_commands(self):
        """Set up the commands."""

        help_cmd = Command("help",
                       " : afficher cette aide",
                       Actions.help, 0)
        self.commands["help"] = help_cmd
        quit_cmd = Command("quit",
                        " : quitter le jeu",
                        Actions.quit, 0)
        self.commands["quit"] = quit_cmd
        go = Command("go",
                     " <direction> : se déplacer dans une direction (N, E, S, O, U, D)", 
                     Actions.go, 1)
        self.commands["go"] = go
        back_cmd = Command("back",
                           " : revenir à la pièce précédente",
                           Actions.back, 0)
        self.commands["back"] = back_cmd
        look_command = Command("look",
                               " : observer la pièce et voir les objets présents",
                               Actions.look, 0)
        self.commands["look"] = look_command
        take_cmd = Command("take",
                           " <item> : prendre un objet",
                           Actions.take, 1)
        self.commands["take"] = take_cmd
        drop_cmd = Command("drop",
                           " <item> : déposer un objet",
                           Actions.drop, 1)
        self.commands["drop"] = drop_cmd
        check_cmd = Command("check",
                            " : afficher l'inventaire",
                            Actions.check, 0)
        self.commands["check"] = check_cmd
        unlock_command = Command("unlock",
                                " <direction> : déverrouiller une porte"
                                " avec la clé correspondante",
                                 Actions.unlock, 1)
        self.commands["unlock"] = unlock_command
        talk_cmd = Command("talk",
                           " <someone> : parler à un personnage",
                           Actions.talk, 1)
        self.commands["talk"] = talk_cmd
        activate_cmd = Command("activate",
                               " <quest> : activer une quête",
                               Actions.activate, 1)
        self.commands["activate"] = activate_cmd
        quests_cmd = Command("quests",
                             " : afficher la liste des quêtes",
                             Actions.quests, 0)
        self.commands["quests"] = quests_cmd
        quest_cmd = Command("quest",
                            " <quest> : afficher les détails d'une quête",
                            Actions.quest, 1)
        self.commands["quest"] = quest_cmd
        rewards_cmd = Command("rewards",
                              " : afficher les récompenses obtenues",
                              Actions.rewards, 0)
        self.commands["rewards"] = rewards_cmd

    def setup_rooms(self):
        """Set up the rooms"""
        self.rooms["esiee"] = Room(
            "Esiee",
            "Lisa est dans la rue de l'esiee, au milieu des étudiants"
        )
        self.rooms["bu"] = Room("Bu",
                  " Lisa est dans la bibliotèque de l'école " \
                  "et vous apercevez Berko au loin")
        self.rooms["rue"] = Room("Rue",
                   "Lisa est dans la rue, de l'air frais enfin")
        self.rooms["magasin"] = Room("Magasin",
                        "Lisa est dans un magasin,"
                        " il y a tout le nécessaire pour une " \
                        "CE (résistances et goûts).")
        self.rooms["chez_amine"]     = Room("Chez Amine",
                         "Lisa est rentré chez Amine")
        self.rooms["couloir"] = Room("Couloir",
                       "Lisa est devant la porte de chez Amine")
        self.rooms["crackheads"] = Room("Crackheads",
                          "Lisa croise des crackheads et se fait " \
                          "planter (29/09/2005 - 21/01/2026)")
        self.rooms["ascenseur2"] = Room("Ascenseur2",
                          "Lisa est dans l'ascenseur, au deuxième " \
                          "étage du crous Monstesquieu")
        self.rooms["ascenseur1"] = Room("Ascenseur1",
                            "Lisa est dans l'ascenseur,"
                            " au premier étage du crous " \
                            "Monstesquieu (Amine vie ici)")
        self.rooms["saad_junior"] = Room("SaadJunior",
                          "Lisa croise saad dans la Junior " \
                          "Entreprise il lui tend ses clés")

        self.rooms["esiee"].exits = {
            "N" : self.rooms["saad_junior"],
            "S" : self.rooms["rue"],
            "O" : self.rooms["bu"],
        }
        self.rooms["bu"].exits = {
            "E" : self.rooms["esiee"],
        }
        self.rooms["rue"].exits = {
            "N" : (self.rooms["esiee"], Door(locked=True, key_name="carte")),
            "E" : self.rooms["ascenseur1"],
            "S" : self.rooms["magasin"],
            "O" : self.rooms["crackheads"],
        }
        self.rooms["magasin"].exits = {
            "N" : self.rooms["rue"],
        }
        self.rooms["chez_amine"].exits = {
            "S" : self.rooms["couloir"],
        }
        self.rooms["couloir"].exits = {
            "N" :  (self.rooms["chez_amine"], Door(locked=True, key_name="clé")),
            "S" : self.rooms["ascenseur2"],
        }
        self.rooms["ascenseur1"].exits = {
            "O" : self.rooms["rue"],
            "U" : self.rooms["ascenseur2"],
        }
        self.rooms["ascenseur2"].exits = {
            "N" : self.rooms["couloir"],
            "D" : self.rooms["ascenseur1"]
        }
        self.rooms["saad_junior"].exits = {
            "S" : self.rooms["esiee"],
        }

    def setup_fail_messages(self):
        """Set up the fail messages for each room."""
        self.rooms["esiee"].fail_messages = {
            "E": "Il y a un mur",
            "U": "Tu veux t'envoler ? Il y a un plafond", 
            "D": "Il n'y a pas de tunnel sous terrain désolé",
        }
        self.rooms["saad_junior"].fail_messages = {
            "E": "Il y a un mur", 
            "O": "Il y a un mur", 
            "N": "Il y a Yann avec un poème à la main, "
            "Lisa fait demi-tour et reste avec Saad.",
            "U": "Tu veux t'envoler ? Il y a un plafond",
            "D": "Il n'y a pas de tunnel sous terrain désolé",
        }
        self.rooms["bu"].fail_messages = {
            "U": "Tu veux t'envoler ?", 
            "D": "Il n'y a pas de tunnel sous terrain désolé", 
        }
        self.rooms["magasin"].fail_messages = {
            "U": "Tu veux t'envoler ?", 
            "D": "Il n'y a pas de tunnel sous terrain désolé", 
        }
        self.rooms["rue"].fail_messages = {
            "U": "Tu veux t'envoler ?", 
            "D": "Il n'y a pas de tunnel sous terrain désolé",
            "N": "Tu n'as pas ta carte étudiante "
            "donc ne peut plus rentrer" 
        }
        self.rooms["couloir"].fail_messages = {
            "U": "Tu veux t'envoler ? Il y a un plafond", 
            "D": "Il n'y a pas de tunnel sous terrain désolé", 
        }
        self.rooms["chez_amine"].fail_messages = {
            "U": "Tu veux t'envoler ? Il y a un plafond", 
            "D": "Il n'y a pas de tunnel sous terrain désolé", 
        }

    def setup_characters(self):
        """Set up the characters."""

        self.characters = []
        saad = Character("Saad", "un ami", self.rooms["saad_junior"], ["slt lisa c'est saad"])
        amine = Character("Amine", "un ami", self.rooms["chez_amine"], ["slt lisa c'est amine"])
        berko = Character("Berko", "un ami", self.rooms["bu"], ["slt lisa c'est berko"])

        self.characters.extend([saad, amine, berko])
        self.rooms["saad_junior"].characters.append(saad)
        self.rooms["chez_amine"].characters.append(amine)
        self.rooms["bu"].characters.append(berko)

    def setup_items(self):
        """Set up the items."""
        cles = Item("clés",
                    "celles de chez Amine",0.001)
        self.rooms["saad_junior"].items = ["clés"]
        carte = Item("carte",
                     "C'est ta carte étudiante elle " \
                     "te permet de rentrer dans l'école",0.001)
        self.rooms["magasin"].items = ["carte"]
        porte_chez_amine = Door(locked=True, key_name="clés")
        # On remplace l'exit normale par un tuple (room, door)
        self.rooms["couloir"].exits["N"] = (self.rooms["chez_amine"], porte_chez_amine)
        porte_esiee = Door(locked=True, key_name="carte")
        self.rooms["rue"].exits["N"] = (self.rooms["esiee"], porte_esiee)


        # Ajouter les items à certaines salles
        self.rooms["saad_junior"].inventory.add_item(cles)
        self.rooms["magasin"].inventory.add_item(carte)


        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = self.rooms["esiee"]
        self.player.history.append(self.player.current_room)

    def _setup_quests(self):
        """Initialize all quests."""
        amitie = Quest(
            title="badge de l'amitié",
            description="parler à tout le monde",
            objectives=["Parler à Saad"
                        , "Parler à Amine"
                        , "Parler à Berko"],
            reward="du bonheur"
        )

        self.player.quest_manager.add_quest(amitie)


    # Play the game
    def play(self):
        """Play the game."""
        self.setup()
        self._setup_quests()   # ← AJOUTE CETTE LIGNE
        self.print_welcome()

        while not self.finished:
            self.process_command(input("> "))


    def process_command(self, command_string) -> None:
        """Process the command entered by the player."""

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands:
            print("  ")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    def print_welcome(self):
        """Print the welcome message."""
        print(
            f"\nBienvenue {self.player.name}, vous incarnez Lisa une jeune étudiante "
            "de l'Esiee à la recherche d'une CE. Elle est en total manque de nicotine, "
            "vous devez absolument l'aider à en trouver une.\n"
        )
        print("Entrez 'help' si vous avez besoin d'aide. \n")
        #
        print(self.player.current_room.get_long_description())


def main():
    """Main function to start the game."""
    Game().play()

if __name__ == "__main__":
    main()
