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



from room import Room, Door
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
        self.setup_commands2()
        self.setup_rooms()
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

    def setup_commands2(self):
        """
        Setup additional commands.
        """
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
                  "et un livre semble intéressant")
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
                          "Lisa est dans la saad junior " \
                          "de l'école")
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
            "Il faut être au crous pour pouvoir le réaliser"
    )



        self.rooms["bu"].image = "bu.png"
        self.rooms["magasin"].image = "magasin.png"
        self.rooms["esiee"].image = "esiee.png"
        self.rooms["chez_amine"].image = "chez_amine.png"
        self.rooms["saad_junior"].image = "saad_junior.png"
        self.rooms["Parc"].image = "parc.png"
        self.rooms["Crous"].image = "crous.png"
        self.rooms["epi1"].image = "epi1.png"
        self.rooms["rue"].image = "rue.png"
        self.rooms["couloir"].image = "couloir.png"
        self.rooms["ascenseur1"].image = "ascenseur1.png"
        self.rooms["ascenseur2"].image = "ascenseur2.png"
        self.rooms["Rue_2"].image = "rue_2.png"
        self.rooms["Chemin"].image = "chemin.png"
        self.rooms["crackheads"].image = "crackheads.png"


    def setup_characters(self):
        """Set up the characters."""

        self.characters = []
        # Si votre classe Character est définie comme : __init__(self, name, description)
        saad = Character("Saad", "un ami") 
        # Puis vous assignez le reste manuellement :
        saad.current_room = self.rooms["saad_junior"]
        saad.msgs = ["Coucou Lisa..."]
        amine = Character("Amine", "un ami") 
        amine.current_room = self.rooms["chez_amine"]
        amine.msgs = ["salut lisa, demande moi "
        "si jamais tu veux une CE,j'en ai une en plus"]
        berko = Character("Berko", "un ami")
        berko.current_room = self.rooms["bu"]
        berko.msgs = ["Désolé je n'ai pas de CE sur moi,"
        " va voir Saad ou Amine"]
        manon = Character("Manon", "un ami")
        manon.current_room = self.rooms["Parc"]
        manon.msgs = ["Lisaaaa ! J'ai perdu mon chien, "
        "si tu le trouves ramène le au parc"]
        pablo = Character("Pablo", "un ami")
        pablo.current_room = self.rooms["esiee"]
        pablo.msgs = ["Ok je vois, si tu me ramènes "
        "un cookie je te passe 10€ pour que tu t'achètes une résistance"]


        self.characters.extend([saad, amine, berko, manon, pablo])
        self.rooms["saad_junior"].characters.append(saad)
        self.rooms["chez_amine"].characters.append(amine)
        self.rooms["bu"].characters.append(berko)
        self.rooms["Parc"].characters.append(manon)
        self.rooms["esiee"].characters.append(pablo)



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
                        , "Parler à Pablo"],
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
            reward="Fin du jeu"
        )

        gout = Quest(
            title="fabriquer un gout",
            description="fabriquer un gout pour la CE de Lisa",
            objectives=[
                "trouver les ingredients pour faire un gout",
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
    """Tkinter GUI for the text-based adventure game."""

    IMAGE_WIDTH = 600
    IMAGE_HEIGHT = 600

    def __init__(self):
        super().__init__()

        self._configure_window()

        # Grouped attributes (fix R0902)
        self.widgets = {}
        self.images = {}

        self.game = Game()
        self.game.gui = self

        self._init_player()
        self._build_layout()

        self.original_stdout = sys.stdout
        sys.stdout = _StdoutRedirector(self.widgets["text_output"])

        self.game.print_welcome()
        self._update_room_image()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ---------- Init helpers ----------

    def _configure_window(self):
        self.title("TBA")
        self.geometry("900x700")
        self.minsize(900, 650)

    def _init_player(self):
        name = simpledialog.askstring("Nom", "Entrez votre nom:", parent=self) or "Joueur"
        self.game.setup()          # FIX E1123
        self.game.player.name = name

    # ---------- Layout ----------

    def _build_layout(self):
        self._configure_grid()
        self._build_top()
        self._build_terminal()
        self._build_entry()

    def _configure_grid(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _build_top(self):
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        frame.grid_columnconfigure(1, weight=1)

        self._build_image_area(frame)
        self._build_buttons(frame)

    def _build_image_area(self, parent):
        canvas = tk.Canvas(
            parent,
            width=self.IMAGE_WIDTH,
            height=self.IMAGE_HEIGHT,
            bg="#222"
        )
        canvas.grid(row=0, column=0, padx=(0, 6))
        self.widgets["canvas"] = canvas
        self.images["room"] = None

    # ---------- Buttons ----------

    def _build_buttons(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=1, sticky="ne")
        self._load_button_images()

        self._add_button(frame, "Help", "help", (0, 0))
        self._add_button(frame, "Quit", "quit", (0, 1))

        self._build_directions(frame)

    def _load_button_images(self):
        assets = Path(__file__).parent / "assets"
        names = {
            "help": "help-50.png",
            "quit": "quit-50.png",
            "north": "north-arrow-50.png",
            "south": "south-arrow-50.png",
            "left": "left-arrow-50.png",
            "right": "right-arrow-50.png",
            "up": "up-50.png",
            "down": "down-50.png",
            "back": "back-50.png",
            "look": "look-50.png",
        }

        for key, filename in names.items():
            try:
                self.images[key] = tk.PhotoImage(file=assets / filename)
            except (tk.TclError, FileNotFoundError):
                self.images[key] = None

    def _add_button(self, parent, text, command, position):
        row, col = position
        image = self.images.get(command)
        kwargs = {"image": image} if image else {"text": text}
        tk.Button(
            parent,
            **kwargs,
            command=lambda c=command: self._send_command(c),
            bd=0
        ).grid(row=row, column=col, padx=2)

    def _build_directions(self, parent):
        frame = ttk.LabelFrame(parent, text="Directions")
        frame.grid(row=1, column=0, columnspan=2, pady=4)

        directions = {
            "N": ("north", 0, 1),
            "S": ("south", 2, 1),
            "O": ("left", 1, 0),
            "E": ("right", 1, 2),
            "U": ("up", 0, 0),
            "D": ("down", 2, 0),
            "back": ("back", 2, 2),
            "look": ("look", 0, 2),
        }

        for cmd, (img, r, c) in directions.items():
            self._add_direction_button(frame, cmd, img, (r, c))

    def _add_direction_button(self, parent, cmd, img_key, position):
        row, col = position
        image = self.images.get(img_key)
        kwargs = {"image": image} if image else {"text": cmd}
        tk.Button(
            parent,
            **kwargs,
            command=lambda c=cmd: self._send_command(f"go {c}" if len(c) == 1 else c),
            bd=0
        ).grid(row=row, column=col)

    # ---------- Terminal ----------

    def _build_terminal(self):
        frame = ttk.Frame(self)
        frame.grid(row=1, column=0, sticky="nsew", padx=6)

        text = tk.Text(frame, state="disabled", bg="#111", fg="#eee", wrap="word")
        text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, command=text.yview)
        scrollbar.pack(side="right", fill="y")
        text.config(yscrollcommand=scrollbar.set)

        self.widgets["text_output"] = text

    def _build_entry(self):
        frame = ttk.Frame(self)
        frame.grid(row=2, column=0, sticky="ew", padx=6, pady=6)

        var = tk.StringVar()
        entry = ttk.Entry(frame, textvariable=var)
        entry.pack(fill="x")
        entry.bind("<Return>", self._on_enter)

        self.widgets["entry"] = entry
        self.widgets["entry_var"] = var

    # ---------- Game interaction ----------

    def _on_enter(self, _event=None):
        value = self.widgets["entry_var"].get().strip()
        if value:
            self._send_command(value)
        self.widgets["entry_var"].set("")

    def _send_command(self, command):
        if self.game.finished:
            return
        print(f"> {command}\n")
        self.game.process_command(command)
        self._update_room_image()

    def _update_room_image(self):
        room = getattr(self.game.player, "current_room", None)
        if not room:
            return

        canvas = self.widgets["canvas"]
        canvas.delete("all")
        canvas.create_text(
            self.IMAGE_WIDTH // 2,
            self.IMAGE_HEIGHT // 2,
            text=room.name,
            fill="white",
            font=("Helvetica", 18),
        )

    def _on_close(self):
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
