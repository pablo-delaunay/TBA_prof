"""
Ce module contient la classe Actions qui définit toutes les commandes
exécutables par le joueur dans le jeu.
"""

from item import Item

MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:
    """Classe contenant les actions associées aux commandes du jeu."""

    @staticmethod
    def go(game, list_of_words, number_of_parameters):
        """Déplace le joueur dans la direction spécifiée."""
        player = game.player

        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        direction = list_of_words[1].upper()

        # Logique spécifique au Chemin
        if player.current_room == game.rooms.get("Chemin") and direction == "O":
            if not Actions._handle_crackheads(game):
                return False

        direction_norm = Actions._get_direction(list_of_words[1])
        if not direction_norm:
            print("\nDirection inconnue. Utilisez N, E, S, O, U, D.\n")
            return False

        exit_info = player.current_room.get_exit(direction_norm)
        if exit_info is None:
            print("\nImpossible d'aller dans cette direction.\n")
            return False

        # Gestion des portes verrouillées
        next_room = exit_info
        if isinstance(exit_info, tuple):
            next_room, door = exit_info
            if door.locked:
                print("\n🚪 La porte est verrouillée. Utilisez 'unlock <direction>'.\n")
                return False

        # Exécution du déplacement
        player.current_room = next_room
        player.history.append(next_room)

        Actions._display_move_results(player, next_room)
        Actions._move_characters(game, player)

        return True

    @staticmethod
    def _handle_crackheads(game):
        """Gère l'événement dangereux dans le chemin."""
        print("Titouan : Lisa il y a des crackheads là-bas, tu es sûre d'y aller ?")
        answer = game.get_input("(oui / non) > ").lower().strip()
        if answer == "oui":
            print("\nLisa est morte tuée.")
            game.finished = True
        else:
            print("\nTu restes dans le chemin.")
        return False

    @staticmethod
    def _display_move_results(player, next_room):
        """Affiche les informations suite à un déplacement."""
        hist = player.get_history()
        if hist:
            print(hist)
        print(next_room.get_long_description())
        if getattr(next_room, "is_shop", False):
            print("\n🛒 Le magasin propose :")
            for item in next_room.inventory.items:
                print(f" - {item.name} ({item.price}€)")

    @staticmethod
    def _move_characters(game, player):
        """Déplace les personnages non-joueurs."""
        for char in game.characters:
            moved, old_room = char.move()
            if moved and old_room == player.current_room:
                print(f"{char.name} s'est déplacé.")

    @staticmethod
    def _get_direction(direction_str):
        """Convertit une chaîne en direction standard."""
        synonyms = {
            "N": "N", "NORD": "N", "E": "E", "EST": "E",
            "S": "S", "SUD": "S", "O": "O", "OUEST": "O",
            "U": "U", "UP": "U", "D": "D", "DOWN": "D"
        }
        return synonyms.get(direction_str.upper())

    @staticmethod
    def quit(game, list_of_words, number_of_parameters):
        """Quitte le jeu proprement."""
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False
        print(f"\nMerci {game.player.name} d'avoir joué. Au revoir.\n")
        game.finished = True
        return True

    @staticmethod
    def back(game, _list_of_words, _number_of_parameters):
        """Revient à la salle précédente."""
        player = game.player
        if len(player.history) <= 1:
            print("\nVous ne pouvez pas revenir en arrière.\n")
            return
        player.history.pop()
        player.current_room = player.history[-1]
        hist = player.get_history()
        if hist:
            print(hist)
        print(f"\n{player.current_room.name}\n")

    @staticmethod
    def help(game, list_of_words, number_of_parameters):
        """Affiche les commandes disponibles."""
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print(f"\t- {command}")
        return True

    @staticmethod
    def look(game, _list_of_words, _number_of_parameters):
        """Examine la pièce actuelle."""
        room = game.player.current_room
        money = getattr(room, "money", 0)
        if money > 0:
            print(f"💰 Vous trouvez {money}€ par terre.")
            game.player.money += money
            room.money = 0

        if room.name.lower() == "bu":
            print("📘 Un livre est posé sur une table. (read livre)")

        if getattr(room, "is_shop", False):
            print("🛒 Des objets sont en vente ici. Utilisez `buy <objet>`.")
        else:
            print(room.get_inventory())

    @staticmethod
    def take(game, list_of_words, _num):
        """Prend un objet dans la pièce."""
        if len(list_of_words) != 2:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        item_name = list_of_words[1].lower()
        player, room = game.player, game.player.current_room
        found = room.inventory.get_item(item_name)

        if not found:
            print(f"\nL'objet '{item_name}' n'est pas ici.\n")
            return False

        if player.get_total_weight() + found.weight > player.status.max_weight:
            print(f"\nTrop lourd ! (max {player.status.max_weight} kg)\n")
            return False

        room.inventory.remove_item(item_name)
        player.inventory.add_item(found)
        print(f"\nVous avez pris '{found.name}'.\n")

        if found.name.lower() == "chien":
            player.quest_manager.complete_objective("Prendre le chien")
        return True

    @staticmethod
    def drop(game, list_of_words, _num):
        """Dépose un objet dans la pièce."""
        if len(list_of_words) != 2:
            print("\nPrécisez l'objet à déposer.\n")
            return
        item_name = list_of_words[1].lower()
        item = game.player.inventory.remove_item(item_name)
        if not item:
            print(f"\nVous n'avez pas '{item_name}'.\n")
            return
        game.player.current_room.inventory.add_item(item)
        print(f"\nVous avez déposé '{item.name}'.\n")

    @staticmethod
    def check(game, list_of_words, _num):
        """Affiche l'inventaire du joueur."""
        if len(list_of_words) != 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False
        print("\n" + game.player.inventory.get_inventory() + "\n")
        return True

    @staticmethod
    def talk(game, list_of_words, _num):
        """Parle à un personnage."""
        if len(list_of_words) != 2:
            print("Utilisation : talk <nom>")
            return
        target_name = list_of_words[1].lower()
        target = next((c for c in game.player.current_room.characters
                      if c.name.lower() == target_name), None)
        if not target:
            print(f"{target_name} n'est pas ici.")
            return
        target.get_msg()
        if target.name == "Pablo":
            game.player.quest_manager.activate_quest("Mission Pablo")
        game.player.quest_manager.complete_objective(f"Parler à {target.name}")

    @staticmethod
    def quests(game, list_of_words, number_of_parameters):
        """Affiche la liste des quêtes."""
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False
        game.player.quest_manager.show_quests()
        return True

    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """Affiche les détails d'une quête."""
        if len(list_of_words) < number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False
        title = " ".join(list_of_words[1:])
        counts = {"Se déplacer": game.player.move_count}
        game.player.quest_manager.show_quest_details(title, counts)
        return True

    @staticmethod
    def create(game, list_of_words, _number_of_parameters):
        """Crée un objet 'gout' au Crous."""
        player = game.player
        if len(list_of_words) != 2 or list_of_words[1].lower() != "gout":
            print("❌ Tapez : create gout")
            return False

        if player.current_room != game.rooms.get("Crous"):
            print("❌ Allez au Crous pour cela.")
            return False

        if not (player.inventory.has_item("base") and player.inventory.has_item("cerise")):
            print("❌ Il vous faut une base et des cerises.")
            return False

        player.inventory.remove_item("base")
        player.inventory.remove_item("cerise")
        player.inventory.add_item(Item("gout", "Fait maison", 0.005, 0))
        player.quest_manager.complete_objective("Créer un gout")
        print("✨ Vous avez créé un gout !")
        return True

    @staticmethod
    def buy(game, list_of_words, _num):
        """Achète un objet au magasin."""
        room, player = game.player.current_room, game.player
        if room.name.lower() != "magasin":
            print("❌ Allez au magasin.")
            return
        item = room.inventory.get_item(list_of_words[1])
        if item and player.money >= item.price:
            player.money -= item.price
            room.inventory.remove_item(item.name)
            player.inventory.add_item(item)
            print(f"🛒 Achat de {item.name}.")
    @staticmethod
    def unlock(game, list_of_words, _number_of_parameters):
        """
        Déverrouille une porte si le joueur possède la clé correspondante.

        Args:
            game (Game): L'objet jeu.
            list_of_words (list[str]): La commande et la direction de la porte.
            _number_of_parameters (int): Non utilisé.
        """
        if len(list_of_words) != 2:
            print("Utilisation : unlock <direction>")
            return

        direction_raw = list_of_words[1]
        direction = Actions._get_direction(direction_raw)

        if not direction:
            print(f"\n'{direction_raw}' n'est pas une direction valide.\n")
            return

        room = game.player.current_room
        exit_info = room.get_exit(direction)

        # Vérification de l'existence d'une porte
        if not isinstance(exit_info, tuple):
            print(f"Il n'y a pas de porte verrouillée vers le {direction_raw}.")
            return

        _, door = exit_info

        if not door.locked:
            print("La porte est déjà déverrouillée.")
            return

        # Vérification de la clé
        if not game.player.inventory.has_item(door.key_name):
            print(f"Il vous faut la clé '{door.key_name}' pour ouvrir cette porte.")
            return

        # Action de déverrouillage
        door.locked = False
        print(f"🔓 Vous insérez la clé '{door.key_name}'..."\
              "La porte vers le {direction_raw} est ouverte !")

    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
        """
        Active une quête spécifique demandée par le joueur.
        
        Args:
            game (Game): L'objet jeu.
            list_of_words (list): La liste des mots (ex: ["activate", "Mission", "Pablo"]).
            number_of_parameters (int): Le nombre attendu de paramètres.

        Returns:
            bool: True si l'activation est réussie, False sinon.
        """
        # Vérification du nombre de paramètres
        if len(list_of_words) < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Reconstruction du titre de la quête (si le nom contient des espaces)
        quest_title = " ".join(list_of_words[1:])

        # Tentative d'activation via le quest_manager du joueur
        success = game.player.quest_manager.activate_quest(quest_title)

        if success:
            print(f"\n✨ La quête '{quest_title}' est maintenant active !")
            return True

        # Message d'erreur si la quête est introuvable ou déjà active
        error_msg = (
            f"\nImpossible d'activer la quête '{quest_title}'.\n"
            "Vérifiez l'orthographe ou si elle n'est pas déjà dans votre journal.\n"
        )
        print(error_msg)
        return False

    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        """
        Affiche la liste des récompenses obtenues par le joueur.
        
        Args:
            game (Game): L'objet jeu.
            list_of_words (list): La liste des mots de la commande.
            number_of_parameters (int): Le nombre de paramètres attendus (0).

        Returns:
            bool: True si la commande a été exécutée, False sinon.
        """
        # Vérification stricte du nombre de paramètres (la commande doit être seule)
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # On délègue l'affichage à la méthode de l'objet Player
        # On suppose que player.show_rewards() gère déjà le print
        print("\n--- 🏆 VOS RÉCOMPENSES ---")
        game.player.show_rewards()
        print("--------------------------\n")

        return True

    @staticmethod
    def give(game, list_of_words, _number_of_parameters):
        """
        Permet au joueur de donner un objet de son inventaire à un personnage présent.

        Args:
            game (Game): L'objet jeu.
            list_of_words (list[str]): La commande (ex: ["give", "cookie", "pablo"]).
            _number_of_parameters (int): Non utilisé ici.
        """
        # 1. Vérification de la syntaxe
        if len(list_of_words) != 3:
            print("Utilisation : give <nom_objet> <nom_personnage>")
            return

        item_name = list_of_words[1].lower()
        target_name = list_of_words[2].lower()
        player = game.player
        room = player.current_room

        # 2. Vérification de la possession de l'objet
        item = player.inventory.get_item(item_name)
        if not item:
            print(f"\nVous n'avez pas de '{item_name}' dans votre inventaire.\n")
            return

        # 3. Recherche du personnage dans la pièce
        target = next((c for c in room.characters if c.name.lower() == target_name), None)
        if not target:
            print(f"\n{target_name} n'est pas ici pour recevoir cela.\n")
            return

        # 4. Transfert de l'objet
        player.inventory.remove_item(item_name)
        target.receive_item(item)
        print(f"\n🎁 Vous donnez '{item.name}' à {target.name}.\n")

        # 5. Gestion des objectifs de quête
        Actions._check_give_objectives(game, item.name.lower(), target.name.lower())

    @staticmethod
    def _check_give_objectives(game, item_id, target_id):
        """Vérifie si le don remplit un objectif spécifique."""
        if item_id == "cookie" and target_id == "pablo":
            game.player.quest_manager.complete_objective("Ramener le cookie à Pablo")

    @staticmethod
    def money(game, list_of_words, number_of_parameters):
        """
        Affiche la quantité d'argent possédée par le joueur.

        Args:
            game (Game): L'objet jeu.
            list_of_words (list[str]): La liste des mots de la commande.
            number_of_parameters (int): Le nombre attendu de paramètres (0).

        Returns:
            bool: True si la commande a été exécutée, False sinon.
        """
        # Vérification qu'aucun paramètre n'est fourni (ex: juste "money")
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # On appelle la méthode d'affichage du joueur
        # Si vous n'avez pas de méthode show_money, utilisez le print ci-dessous
        player = game.player
        print(f"\n💰 Portefeuille : {player.money}€\n")

        return True

    @staticmethod
    def sell(game, list_of_words, _number_of_parameters):
        """
        Permet au joueur de vendre un objet de son inventaire lorsqu'il est au magasin.

        Args:
            game (Game): L'objet jeu.
            list_of_words (list[str]): La commande (ex: ["sell", "resistance"]).
            _number_of_parameters (int): Non utilisé.
        """
        player = game.player
        room = player.current_room

        # 1. Vérification du lieu
        if room.name.lower() != "magasin":
            print("\n❌ Vous devez être dans le magasin pour vendre vos objets.\n")
            return

        # 2. Vérification de la syntaxe
        if len(list_of_words) != 2:
            print("Utilisation : sell <nom_objet>")
            return

        item_name = list_of_words[1].lower()
        item = player.inventory.get_item(item_name)

        # 3. Vérification de la possession
        if not item:
            print(f"\nVous ne possédez pas '{item_name}' dans votre inventaire.\n")
            return

        # 4. Calcul du prix de revente (50% du prix original)
        sell_price = item.price // 2

        # 5. Transaction
        player.inventory.remove_item(item_name)
        room.inventory.add_item(item)
        player.money += sell_price

        print(f"\n💰 Vous avez vendu '{item.name}' pour {sell_price}€.")
        print(f"Votre nouveau solde est de {player.money}€.\n")

    @staticmethod
    def ask(game, words, _num_params):
        """
        Demande un objet à un personnage.
        
        Args:
            game (Game): L'objet jeu.
            words (list[str]): La commande (ex: ["ask", "ce", "pablo"]).
            _num_params (int): Non utilisé.
        """
        if len(words) != 3:
            print("Utilisation : ask <objet> <personnage>")
            return

        item_name = words[1].lower()
        target_name = words[2].lower()
        player = game.player

        # 1. Trouver le personnage dans la pièce actuelle
        target = next((c for c in player.current_room.characters
                      if c.name.lower() == target_name), None)

        if not target:
            print(f"\n{target_name} n'est pas ici.\n")
            return

        # 2. Vérifier si le personnage possède l'objet
        item = target.inventory.get_item(item_name)
        if not item:
            print(f"\n{target.name} n'a pas de '{item_name}' à vous donner.\n")
            return

        # 3. Vérification du poids pour le joueur
        if player.get_total_weight() + item.weight > player.status.get("max_weight", 10):
            print(f"\nL'objet '{item.name}' est trop lourd pour vous.\n")
            return

        # 4. Transfert de l'objet
        target.inventory.remove_item(item_name)
        player.inventory.add_item(item)
        print(f"\n🤝 {target.name} vous donne '{item.name}'.")

        # 5. Objectifs de quête
        if item.name.lower() == "ce":
            player.quest_manager.complete_objective("Avoir une CE dans l'inventaire")

    @staticmethod
    def read(game, words, _num_params):
        """
        Permet au joueur de lire un objet spécifique dans la pièce ou l'inventaire.

        Args:
            game (Game): L'objet jeu.
            words (list[str]): La commande (ex: ["read", "livre"]).
            _num_params (int): Non utilisé.
        """
        if len(words) != 2:
            print("Utilisation : read <objet>")
            return

        target = words[1].lower()
        player = game.player
        room = player.current_room

        # 1. Lecture d'un objet spécifique à la salle (ex: Livre dans la BU)
        if target == "livre" and hasattr(room, "book_text"):
            print(f"\n📖 Vous ouvrez le livre :\n{'-'*20}")
            print(room.book_text)
            print(f"{'-'*20}\n")
            return

        # 2. Lecture d'un objet dans l'inventaire (ex: un journal)
        item = player.inventory.get_item(target)
        if item and hasattr(item, "content"):
            print(f"\n📝 Contenu de {item.name} :\n{item.content}\n")
            return

        # 3. Cas par défaut
        if target == "livre":
            print("\nIl n'y a pas de livre ici, ou celui-ci est illisible.\n")
        else:
            print(f"\nIl n'y a rien d'intéressant à lire sur '{target}'.\n")
