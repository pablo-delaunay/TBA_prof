" Main game class"

# Import modules
from pathlib import Path
import sys

# Tkinter imports for GUI
try:
    import tkinter as tk
    from tkinter import ttk, simpledialog
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

# PIL imports for image handling
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


from room import Room
from room import Door
from player import Player
from command import Command
from actions import Actions
from item import Inventory, Item
from character import Character
from quests import Quest

class Game:
    """Main game class."""
    def __init__(self):
        """Initialize the game state."""
        self.finished = False
        self.rooms = {}
        self.commands = {}
        self.player = None
        self.characters = []
        self.player_name = "Joueur"


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
        give_cmd = Command(
            "give",
            " <item> <character> : donner un objet à un personnage",
            Actions.give, 2
        )
        self.commands["give"] = give_cmd
        money_cmd = Command(
            "money",
            " : afficher l'argent du joueur",
            Actions.money, 0
        )
        self.commands["money"] = money_cmd
        buy_cmd = Command(
            "buy",
            " <item> : acheter un objet au magasin",
            Actions.buy,
            1
        )
        self.commands["buy"] = buy_cmd
        sell_cmd = Command(
            "sell",
            " <item> : vendre un objet au magasin",
            Actions.sell,
            1
        )
        self.commands["sell"] = sell_cmd
        ask_cmd = Command(
            "ask",
            " <item> <character> : demander un objet à un personnage",
            Actions.ask,
            2
        )
        self.commands["ask"] = ask_cmd
        read_cmd = Command(
            "read",
            " <objet> : lire quelque chose",
            Actions.read,
            1
        )
        self.commands["read"] = read_cmd
        create_cmd = Command(
            "create",
            " <item> : créer un objet si vous avez les ingrédients nécessaires",
            Actions.create,
            1
        )
        self.commands["create"] = create_cmd

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
        self.rooms["chez_amine"] = Room("Chez Amine",
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
        self.rooms["Parc"] = Room("Parc",
                       "Lisa est dans le parc, il y a plein " \
                       "d'étudiants qui fument des CE ici")
        self.rooms["Chemin"] = Room("Chemin",
                       "Lisa est dans le chemin entre le parc et " \
                       "l'autre coté de l'école")
        self.rooms["Rue_2"] = Room("Rue_2",
                       "Lisa est dans la rue dèrriere l'école")
        self.rooms["Crous"] = Room("Crous",
                       "Lisa est dans le crous")
        self.rooms["epi1"] = Room("epi1",
                       "Lisa est dans l'epi1 à l'étage")

        self.rooms["esiee"].exits = {
            "N" : self.rooms["saad_junior"],
            "S" : self.rooms["rue"],
            "O" : self.rooms["bu"],
            "U" : self.rooms["epi1"],
        }
        self.rooms["bu"].exits = {
            "E" : self.rooms["esiee"],
        }
        self.rooms["rue"].exits = {
            "N" : (self.rooms["esiee"], Door(locked=True, key_name="carte")),
            "E" : self.rooms["ascenseur1"],
            "S" : self.rooms["magasin"],
            "O" : self.rooms["Parc"],
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
            "N" : self.rooms["Rue_2"],
            "E" : self.rooms["Crous"],
        }
        self.rooms["crackheads"].exits = {
            "E" : self.rooms["Chemin"],
        }
        self.rooms["Parc"].exits = {
            "N" : self.rooms["Chemin"],
            "E" : self.rooms["rue"],
        }
        self.rooms["Chemin"].exits = {
            "S" : self.rooms["Parc"],
            "E" : self.rooms["Rue_2"],
            "O" : self.rooms["crackheads"],
        }
        self.rooms["Rue_2"].exits = {
            "O" : self.rooms["Chemin"],
            "S" : self.rooms["saad_junior"],
        }
        self.rooms["Crous"].exits = {
            "O" : self.rooms["saad_junior"],
        }
        self.rooms["epi1"].exits = {
            "D" : self.rooms["esiee"],
        }

        self.rooms["magasin"].is_shop = True
        self.rooms["bu"].book_text = (
            "Vous trouvez un livre vous expliquant comment faire votre propre gout\n"
            "« Pour faire votre gout :\n"
            " - de la base ( sans doute au crous )\n"
            " - des cerises ( dans le magasin ) »\n"
    )


        self.rooms["bu"].image = "bu.png"
        self.rooms["magasin"].image = "magasin.png"
        self.rooms["esiee"].image = "esiee.png"
        self.rooms["rue"].image = "rue.png"
        self.rooms["chez_amine"].image = "chez_amine.png"
        self.rooms["couloir"].image = "couloir.png"
        self.rooms["crackheads"].image = None  # No image for crackheads
        self.rooms["ascenseur1"].image = "ascenseur1.png"
        self.rooms["ascenseur2"].image = "ascenseur2.png"
        self.rooms["saad_junior"].image = "saad_junior.png"
        self.rooms["Parc"].image = "parc.png"
        self.rooms["Chemin"].image = "chemin.png"
        self.rooms["Rue_2"].image = "rue_2.png"
        self.rooms["Crous"].image = "crous.png"
        self.rooms["epi1"].image = "epi1.png"

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
        saad = Character("Saad", "un ami", self.rooms["saad_junior"], ["Coucou Lisa, si tu veux aller chez "
        "Amine j'ai posé les clés sur le bureau"])
        amine = Character("Amine", "un ami", self.rooms["chez_amine"], ["slt lisa c'est amine"])
        berko = Character("Berko", "un ami", self.rooms["bu"], ["Désolé je n'ai pas de CE sur moi,"
        " va voir Saad ou Amine"])
        manon = Character("Manon", "un ami", self.rooms["Parc"], ["Lisaaaa ! J'ai perdu mon chien, "
        "si tu le trouves ramène le au parc"])
        pablo = Character("Pablo", "un ami", self.rooms["esiee"], ["Ok je vois, si tu me ramènes un cookie je te"
        " passe 10€ pour que tu t'achètes une résistance"])
        titouan = Character("Titouan", "un ami", self.rooms["Chemin"], ["slt lisa c'est titouan"])


        self.characters.extend([saad, amine, berko, manon, pablo, titouan])
        self.rooms["saad_junior"].characters.append(saad)
        self.rooms["chez_amine"].characters.append(amine)
        self.rooms["bu"].characters.append(berko)
        self.rooms["Parc"].characters.append(manon)
        self.rooms["esiee"].characters.append(pablo)
        self.rooms["Chemin"].characters.append(titouan)


        amine.inventory = Inventory()  # Ajoute un inventaire à Amine
        ce = Item("CE", "Vous possédez une cigarette électronique", 0.001, price=0)
        amine.inventory.add_item(ce)   # Met la CE dans l'inventaire d'Amine

        

    def setup_items(self):
        """Set up the items."""
        cles = Item("clés",
                    "celles de chez Amine",0.001)
        self.rooms["saad_junior"].items = ["clés"]
        carte = Item("carte",
                     "C'est ta carte étudiante elle " \
                     "te permet de rentrer dans l'école",0.001)
        self.rooms["Parc"].items = ["carte"]
        chien = Item("chien",
                    "il est très triste rapporte le a Manon"\
                    " le plus vite possible.", 5)
        self.rooms["Rue_2"].items = ["chien"]
        base = Item("base",
                    "de la base pour faire un gout", 0.5)
        self.rooms["epi1"].money = 5

        porte_chez_amine = Door(locked=True, key_name="clés")
        self.rooms["couloir"].exits["N"] = (self.rooms["chez_amine"], porte_chez_amine)
        porte_esiee = Door(locked=True, key_name="carte")
        self.rooms["rue"].exits["N"] = (self.rooms["esiee"], porte_esiee)


        # Ajouter les items à certaines salles
        self.rooms["saad_junior"].inventory.add_item(cles)
        self.rooms["Parc"].inventory.add_item(carte)
        self.rooms["Rue_2"].inventory.add_item(chien)
        self.rooms["Crous"].inventory.add_item(base)
        self.rooms["epi1"].money = 5

        resistance = Item(
            "résistance",
            "Une résistance pour CE",
            0.01,
            price=10
        )
        cigarette_electronique = Item(
            "cigarette électronique",
            "Une cigarette électronique",
            0.2,
            price=50
        )

        gout = Item(
            "gout",
            "Un gout pour CE",
            0.005,
            price=10
        )

        cerise = Item(
            "cerise",
            "Des cerises pour faire un gout",
            0.2,
            price=5
        )

        self.rooms["magasin"].inventory.add_item(resistance)
        self.rooms["magasin"].inventory.add_item(cigarette_electronique)
        self.rooms["magasin"].inventory.add_item(gout)
        self.rooms["magasin"].inventory.add_item(cerise)

        self.player = Player(self.player_name)
        self.player.current_room = self.rooms["esiee"]
        self.player.history.append(self.player.current_room)

      

    def _setup_quests(self):
        """Initialize all quests."""
        amitie = Quest(
            title="Badge de l'amitié",
            description="parler à tout le monde",
            objectives=["Parler à Saad"
                        , "Parler à Amine"
                        , "Parler à Berko"
                        , "Parler à Manon"
                        , "Parler à Pablo"
                        , "Parler à Titouan"],
            reward="du bonheur"
        )

        manon = Quest(
            title="Aider Manon",
            description="Manon a besoin de votre aide. Retrouvez son chien.",
            objectives=[
                "Prendre le chien",
                "Ramener le chien au parc"
            ],
        reward={
            "type": "item",
            "name": "cookie",
            "weight": 0.2
        }
)

        pablo = Quest(
            title="Mission Pablo",
            description="Pablo veut un cookie, aide le a en trouver un.",
            objectives=[
                "Ramener le cookie à Pablo"
            ],
    reward={
        "type": "money",
        "amount": 10
    }
)
        final = Quest(
            title="Finir le jeu",
            description="Trouver une cigarette électronique, un gout et une résistance pour Lisa.",
            objectives=[
                "Avoir une CE dans l'inventaire",
                "Avoir un gout dans l'inventaire",
                "Avoir une résistance dans l'inventaire"
            ],
            reward={"type": "finish_game"}
        )

        gout = Quest(
            title="fabriquer un gout",
            description="fabriquer un gout pour la CE de Lisa",
            objectives=[
                "Avoir une base dans l'inventaire",
                "Avoir des cerises dans l'inventaire",
                "creer le gout",
            ],
            reward={
                "type": "item",
                "name": "gout",
                "weight": 0.005
            }
        )

        self.player.quest_manager.add_quest(amitie)
        self.player.quest_manager.add_quest(manon)
        self.player.quest_manager.add_quest(pablo)
        self.player.quest_manager.add_quest(final)
        self.player.quest_manager.add_quest(gout)


    # Play the game
    def play(self):
        """Play the game."""
        self.setup()
        self._setup_quests()
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

    def get_input(self, prompt=""):
        """Get user input, handling both CLI and GUI modes."""
        try:
            # Try to use GUI dialog if available
            if hasattr(self, 'gui') and self.gui:
                result = simpledialog.askstring("Input", prompt)
                return result if result else ""
        except:
            pass
        # Fallback to standard input
        return input(prompt)

##############################
# Tkinter GUI Implementation #
##############################

class _StdoutRedirector:
    """Redirect sys.stdout writes into a Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, msg):
        """Write message to the Text widget."""
        if msg:
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", msg)
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")

    def flush(self):
        """Flush method required by sys.stdout interface (no-op for Text widget)."""


class GameGUI(tk.Tk):
    """Tkinter GUI for the text-based adventure game.

    Layout layers:
    L3 (top): Split into left image area (600x400) and right buttons.
    L2 (middle): Scrolling terminal output.
    L1 (bottom): Command entry field.
    """

    IMAGE_WIDTH = 600
    IMAGE_HEIGHT = 600

    def __init__(self):
        super().__init__()
        self.title("TBA")
        self.geometry("900x700")  # Provide enough space
        self.minsize(900, 650)

        # Underlying game logic instance
        self.game = Game()
        self.game.gui = self  # Set GUI reference for input handling

        # Ask player name via dialog (fallback to 'Joueur')
        name = simpledialog.askstring("Nom", "Entrez votre nom:", parent=self)
        if not name:
            name = "Joueur"
        self.game.player_name = name  # Set the player name before setup
        self.game.setup()  # Pass name to avoid double prompt
        self.game._setup_quests()  # Initialize quests

        # Build UI layers
        self._build_layout()

        # Redirect stdout so game prints appear in terminal output area
        self.original_stdout = sys.stdout
        sys.stdout = _StdoutRedirector(self.text_output)

        # Print welcome text in GUI
        self.game.print_welcome()

        # Load initial room image
        self._update_room_image()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)


    # -------- Layout construction --------
    def _build_layout(self):
        # Configure root grid: 3 rows (L3, L2, L1)
        self.grid_rowconfigure(0, weight=0)  # Image/buttons fixed height
        self.grid_rowconfigure(1, weight=1)  # Terminal output expands
        self.grid_rowconfigure(2, weight=0)  # Entry fixed
        self.grid_columnconfigure(0, weight=1)

        # L3 Top frame
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=(6,3))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)

        # L3L Image area (left)
        image_frame = ttk.Frame(top_frame, width=self.IMAGE_WIDTH, height=self.IMAGE_HEIGHT)
        image_frame.grid(row=0, column=0, sticky="nw", padx=(0,6))
        image_frame.grid_propagate(False)  # Keep requested size
        self.canvas = tk.Canvas(image_frame,
                                width=self.IMAGE_WIDTH,
                                height=self.IMAGE_HEIGHT,
                                bg="#222")
        self.canvas.pack(fill="both", expand=True)

        # Initialize image reference (will be loaded by _update_room_image)
        self._image_ref = None  # Keep reference to prevent garbage collection
        # Initial image will be loaded after welcome message

        # L3R Buttons area (right)
        buttons_frame = ttk.Frame(top_frame)
        buttons_frame.grid(row=0, column=1, sticky="ne")
        for i in range(10):
            buttons_frame.grid_rowconfigure(i, weight=0)
        buttons_frame.grid_columnconfigure(0, weight=1)

        # Load button images (keep references to prevent garbage collection)
        assets_dir = Path(__file__).parent / 'assets'
        # Load pre-resized 50x50 PNG images for better quality
        try:
            self._btn_help = tk.PhotoImage(file=str(assets_dir / 'help-50.png'))
        except (FileNotFoundError, tk.TclError):
            self._btn_help = None
        try:
            self._btn_north = tk.PhotoImage(file=str(assets_dir / 'north-arrow-50.png'))
        except (FileNotFoundError, tk.TclError):
            self._btn_north = None
        try:
            self._btn_south = tk.PhotoImage(file=str(assets_dir / 'south-arrow-50.png'))
        except (FileNotFoundError, tk.TclError):
            self._btn_south = None
        try:
            self._btn_left = tk.PhotoImage(file=str(assets_dir / 'left-arrow-50.png'))
        except (FileNotFoundError, tk.TclError):
            self._btn_left = None
        try:
            self._btn_right = tk.PhotoImage(file=str(assets_dir / 'right-arrow-50.png'))
        except (FileNotFoundError, tk.TclError):
            self._btn_right = None
        try:
            self._btn_quit = tk.PhotoImage(file=str(assets_dir / 'quit-50.png'))
        except (FileNotFoundError, tk.TclError):
            self._btn_quit = None
        try:
            self._btn_back = tk.PhotoImage(file=str(assets_dir / 'back-50.png'))
        except (FileNotFoundError, tk.TclError):
            self._btn_back = None
        try:
            self._btn_up = tk.PhotoImage(file=str(assets_dir / 'up-50.png'))
        except (FileNotFoundError, tk.TclError):
            self._btn_up = None
        try:
            self._btn_down = tk.PhotoImage(file=str(assets_dir / 'down-50.png'))
        except (FileNotFoundError, tk.TclError):
            self._btn_down = None
        try:
            self._btn_look = tk.PhotoImage(file=str(assets_dir / 'look-50.png'))
        except (FileNotFoundError, tk.TclError):
            self._btn_look = None

        # Command buttons
        if self._btn_help:
            tk.Button(buttons_frame,
                      image=self._btn_help,
                      command=lambda: self._send_command("help"),
                      bd=0).grid(row=0, column=0, padx=2)
        else:
            tk.Button(buttons_frame,
                      text="Help",
                      command=lambda: self._send_command("help"),
                      bd=0).grid(row=0, column=0, padx=2)
            
        # Quit button
        if self._btn_quit:
            tk.Button(buttons_frame,
                      image=self._btn_quit,
                      command=lambda: self._send_command("quit"),
                      bd=0).grid(row=0, column=1, padx=2)
        else:
            tk.Button(buttons_frame,
                      text="Quit",
                      command=lambda: self._send_command("quit"),
                      bd=0).grid(row=0, column=1, padx=2)

        # Directions buttons in cross layout
        directions_frame = ttk.LabelFrame(buttons_frame, text="Directions")
        directions_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=4)
        # 3x3 grid for cross: North top, West left, East right, South bottom
        if self._btn_up:
            tk.Button(directions_frame,
                      image=self._btn_up,
                      command=lambda: self._send_command("go U"),
                      bd=0).grid(row=0, column=0)
        else:
            tk.Button(directions_frame,
                      text="U",
                      command=lambda: self._send_command("go U"),
                      bd=0).grid(row=0, column=0)
        if self._btn_north:
            tk.Button(directions_frame,
                      image=self._btn_north,
                      command=lambda: self._send_command("go N"),
                      bd=0).grid(row=0, column=1)
        else:
            tk.Button(directions_frame,
                      text="N",
                      command=lambda: self._send_command("go N"),
                      bd=0).grid(row=0, column=1)
        if self._btn_left:
            tk.Button(directions_frame,
                      image=self._btn_left,
                      command=lambda: self._send_command("go O"),
                      bd=0).grid(row=1, column=0)
        else:
            tk.Button(directions_frame,
                      text="O",
                      command=lambda: self._send_command("go O"),
                      bd=0).grid(row=1, column=0)
        if self._btn_right:
            tk.Button(directions_frame,
                      image=self._btn_right,
                      command=lambda: self._send_command("go E"),
                      bd=0).grid(row=1, column=2)
        else:
            tk.Button(directions_frame,
                      text="E",
                      command=lambda: self._send_command("go E"),
                      bd=0).grid(row=1, column=2)
        if self._btn_down:
            tk.Button(directions_frame,
                      image=self._btn_down,
                      command=lambda: self._send_command("go D"),
                      bd=0).grid(row=2, column=0)
        else:
            tk.Button(directions_frame,
                      text="D",
                      command=lambda: self._send_command("go D"),
                      bd=0).grid(row=2, column=0)
        if self._btn_south:
            tk.Button(directions_frame,
                      image=self._btn_south,
                      command=lambda: self._send_command("go S"),
                      bd=0).grid(row=2, column=1)
        else:
            tk.Button(directions_frame,
                      text="S",
                      command=lambda: self._send_command("go S"),
                      bd=0).grid(row=2, column=1)
        if self._btn_up:
            tk.Button(directions_frame,
                      image=self._btn_up,
                      command=lambda: self._send_command("go U"),
                      bd=0).grid(row=0, column=0)
        else:
            tk.Button(directions_frame,
                      text="U",
                      command=lambda: self._send_command("go U"),
                      bd=0).grid(row=0, column=0)
        if self._btn_back:
            tk.Button(directions_frame,
                      image=self._btn_back,
                      command=lambda: self._send_command("back"),
                      bd=0).grid(row=2, column=2)
        else:
            tk.Button(directions_frame,
                      text="Back",
                      command=lambda: self._send_command("back"),
                      bd=0).grid(row=2, column=2)
        if self._btn_look:
            tk.Button(directions_frame,
                      image=self._btn_look,
                      command=lambda: self._send_command("look"),
                      bd=0).grid(row=0, column=2)
        else:
            tk.Button(directions_frame,
                      text="Look",
                      command=lambda: self._send_command("look"),
                      bd=0).grid(row=0, column=2)

        # L2 Terminal output area (Text + Scrollbar)
        output_frame = ttk.Frame(self)
        output_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=3)
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical")
        self.text_output = tk.Text(output_frame,
                                   wrap="word",
                                   yscrollcommand=scrollbar.set,
                                   state="disabled",
                                   bg="#111", fg="#eee")
        scrollbar.config(command=self.text_output.yview)
        self.text_output.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # L1 Entry area
        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=2, column=0, sticky="ew", padx=6, pady=(3,6))
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(entry_frame, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()


    # -------- Image update --------
    def _update_room_image(self):
        """Update the canvas image based on the current room."""
        if not self.game.player or not self.game.player.current_room:
            return

        room = self.game.player.current_room
        assets_dir = Path(__file__).parent / 'assets'

        # Use room-specific image if available, otherwise fallback
        if room.image:
            image_path = assets_dir / room.image
        else:
            image_path = assets_dir / 'scene.png'

        try:
            if PIL_AVAILABLE:
                # Load and resize image with PIL
                pil_image = Image.open(str(image_path))
                pil_image = pil_image.resize((self.IMAGE_WIDTH, self.IMAGE_HEIGHT), Image.Resampling.LANCZOS)
                self._image_ref = ImageTk.PhotoImage(pil_image)
            else:
                # Load with Tkinter (no resize)
                self._image_ref = tk.PhotoImage(file=str(image_path))
            # Clear canvas and redraw image
            self.canvas.delete("all")
            self.canvas.create_image(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                image=self._image_ref
            )
        except (FileNotFoundError, tk.TclError, OSError):
            # Fallback to text if image not found or cannot be loaded
            self.canvas.delete("all")
            self.canvas.create_text(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                text=f"Image: {room.name}",
                fill="white",
                font=("Helvetica", 18)
            )


    # -------- Event handlers --------
    def _on_enter(self, _event=None):
        """Handle Enter key press in the entry field."""
        value = self.entry_var.get().strip()
        if value:
            self._send_command(value)
        self.entry_var.set("")


    def _send_command(self, command):
        if self.game.finished:
            return
        # Echo the command in output area
        print(f"> {command}\n")
        self.game.process_command(command)
        # Update room image after command (in case player moved)
        self._update_room_image()
        if self.game.finished:
            # Disable further input and schedule close (brief delay to show farewell)
            self.entry.configure(state="disabled")
            self.after(600, self._on_close)


    def _on_close(self):
        # Restore stdout and destroy window
        sys.stdout = self.original_stdout
        self.destroy()



def main():
    """Entry point.

    If '--cli' is passed as an argument, start the classic console version.
    Otherwise launch the Tkinter GUI.
    Fallback to CLI if GUI cannot be initialized (e.g., headless environment).
    """
    args = sys.argv[1:]
    if '--cli' in args:
        Game().play()
        return
    try:
        app = GameGUI()
        app.mainloop()
    except tk.TclError as e:
        # Fallback to CLI if GUI fails (e.g., no DISPLAY, Tkinter not available)
        print(f"GUI indisponible ({e}). Passage en mode console.")
        Game().play()


if __name__ == "__main__":
    main()