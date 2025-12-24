" Actions for the game commands."
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:
    """Classe contenant les actions associées aux commandes du jeu."""
    @staticmethod
    def go(game, list_of_words, number_of_parameters):
        """
        Déplace le joueur dans la direction spécifiée si possible.

        Args:
            game (Game): L'objet jeu contenant l'état actuel.
            list_of_words (list[str]): La commande et ses arguments (ex: ["go", "N"]).
            number_of_parameters (int): Le nombre attendu de paramètres pour la commande.

        Returns:
            bool: True si le déplacement a été effectué, False sinon.
        """
        player = game.player

        # Vérifie le nombre de paramètres
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        direction = Actions._get_direction(list_of_words[1])
        if not direction:
            print("\nDirection inconnue. Utilisez N, E, S, O, U, D.\n")
            return False

        room = player.current_room
        exit_info = room.get_exit(direction)

        if exit_info is None:
            print("\nImpossible d'aller dans cette direction.\n")
            return False

        if isinstance(exit_info, tuple):
            next_room, door = exit_info
            if not Actions._handle_locked_door(game, direction, door):
                return False
        else:
            next_room = exit_info

        # Déplacement du joueur
        player.current_room = next_room
        player.history.append(next_room)

        # Affichage
        print(next_room.get_long_description())
        hist = player.get_history()
        if hist:
            print(hist)

        # Déplacement des personnages
        for char in game.characters:
            moved, old_room = char.move()
            if moved and old_room == player.current_room:
                print(f"{char.name} s'est déplacé.")

        return True

    @staticmethod
    def _get_direction(direction_str):
        """Convertit une chaîne de caractères en direction standard."""
        synonyms = {
            "N": "N", "NORD": "N",
            "E": "E", "EST": "E",
            "S": "S", "SUD": "S",
            "O": "O", "OUEST": "O",
            "U": "U", "UP": "U",
            "D": "D", "DOWN": "D"
        }
        return synonyms.get(direction_str.upper())

    @staticmethod
    def _handle_locked_door(game, direction, door):
        """Gère la porte verrouillée Rue -> Esiee uniquement."""
        if game.player.current_room.name == "Rue" and direction == "N" and door.locked:
            if game.player.inventory.has_item("carte"):
                door.locked = False
                print("\nVotre carte étudiante vous permet d'entrer dans l'Esiee.\n")
                return True

            print("\nVous ne pouvez pas entrer à l'Esiee sans votre carte étudiante.\n")
            return False

        return True

    @staticmethod
    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    @staticmethod
    def back(game, _list_of_words, _number_of_parameters):
        """
        Permet au joueur de revenir à la salle précédente.

        Args:
            game (Game): L'objet jeu.
            _list_of_words (list[str]): La commande et ses arguments (non utilisé).
            _number_of_parameters (int): Le nombre attendu de paramètres (non utilisé).

        Returns:
            None
        """
        player = game.player
        if len(player.history) <= 1:
            print("\nVous ne pouvez pas revenir en arrière.\n")
            return

        # Supprime la salle actuelle de l'historique
        player.history.pop()

        # Revenir à la salle précédente
        player.current_room = player.history[-1]

        # Afficher la description et l'historique
        print(player.current_room.get_long_description())
        hist = player.get_history()
        if hist != "":
            print(hist)

    @staticmethod
    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True

    @staticmethod
    def look(game, _list_of_words, _number_of_parameters):
        """
        Affiche la description complète de la salle actuelle et les objets qu'elle contient.

        Args:
            game (Game): L'objet jeu.

        Returns:
            None
        """
        room = game.player.current_room
        # Affiche la description longue de la salle
        print(room.get_long_description())
        # Affiche les items présents dans la salle
        print(room.get_inventory())


    @staticmethod
    def take(game,list_of_words, _number_of_parameters):
        """
        Affiche la liste des commandes disponibles.

        Args:
            game (Game): L'objet jeu.
            list_of_words (list[str]): La commande et ses arguments.
            number_of_parameters (int): Le nombre attendu de paramètres.

        Returns:
            bool: True si la liste est affichée, False si le nombre de paramètres est incorrect.
        """
        if len(list_of_words) != 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item_name = list_of_words[1].lower()
        player = game.player
        room = player.current_room

        # Chercher l’objet dans la pièce
        found = None
        for item in room.inventory.items:
            if item.name.lower() == item_name:
                found = item
                break

        if found is None:
            print(f"\nL'objet '{item_name}' n'est pas présent dans cette pièce.\n")
            return False

        # Vérifier le poids total après ajout
        if player.get_total_weight() + found.weight > player.status.max_weight:
            print(
                f"\nVous ne pouvez pas prendre '{found.name}'. "
                f"Poids total trop élevé ! (max {player.max_weight} kg)\n"
            )
            return False

        # Déplacer l’objet
        room.inventory.remove_item(item_name)
        player.inventory.add_item(found)

        print(f"\nVous avez pris l'objet '{found.name}'.\n")
        return True


    @staticmethod
    def drop(game, list_of_words, _number_of_parameters):
        """
        Permet au joueur de déposer un objet depuis son inventaire dans la salle.

        Args:
            game (Game): L'objet jeu.
            list_of_words (list[str]): La commande et le nom de l'objet à déposer.
            _number_of_parameters (int): Non utilisé.

        Returns:
            None
        """
        # Vérifier le paramètre manquant
        if len(list_of_words) != 2:
            print("\nVous devez préciser quel objet déposer.\n")
            return

        item_name = list_of_words[1].lower()
        player = game.player

        # Vérifier si l'objet est dans l'inventaire du joueur
        item = player.inventory.remove_item(item_name)

        if item is None:
            print(f"\nVous ne possédez pas l'objet '{item_name}'.\n")
            return

        # Ajouter l'objet dans la pièce actuelle
        room = player.current_room
        room.inventory.add_item(item)

        print(f"\nVous avez déposé l'objet '{item.name}'.\n")

    @staticmethod
    def check(game, list_of_words, _number_of_parameters):
        """
        Affiche l'inventaire du joueur.

        Args:
            game (Game): L'objet jeu.
            list_of_words (list[str]): La commande (aucun argument).
            _number_of_parameters (int): Non utilisé.

        Returns:
            bool: True si l'inventaire est affiché, False si le nombre de paramètres est incorrect.
        """

        # Vérifier le nombre de paramètres
        if len(list_of_words) != 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Récupérer l’inventaire du joueur
        inv = game.player.inventory.get_inventory()

        # Affichage
        print("\n" + inv + "\n")

        return True

    @staticmethod
    def unlock(game, list_of_words, _number_of_parameters):
        """
        Déverrouille une porte si le joueur possède la clé correspondante.

        Args:
            game (Game): L'objet jeu.
            list_of_words (list[str]): La commande et la direction de la porte.
            _number_of_parameters (int): Non utilisé.

        Returns:
            None
        """
        if len(list_of_words) != 2:
            print("Utilisation : unlock <direction>")
            return

        direction = list_of_words[1]
        room = game.player.current_room

        exit_info = room.get_exit(direction)

        if exit_info is None or not isinstance(exit_info, tuple):
            print("Il n'y a pas de porte dans cette direction.")
            return

        door = exit_info

        if not door.locked:
            print("La porte est déjà ouverte.")
            return

        # Vérifier que le joueur possède l'objet clé correspondant
        if not game.player.inventory.has_item(door.key_name):
            print(f"Vous n'avez pas la clé '{door.key_name}'.")
            return

        # Déverrouillage
        door.locked = False
        print(f"Vous avez déverrouillé la porte vers {direction}.")

    @staticmethod
    def talk(game, list_of_words, _number_of_parameters):
        """
        Permet au joueur de parler à un personnage dans la salle.

        Args:
            game (Game): L'objet jeu.
            list_of_words (list[str]): La commande et le nom du personnage.
            _number_of_parameters (int): Non utilisé.

        Returns:
            None
        """
        if len(list_of_words) != 2:
            print("Utilisation : talk <nom du personnage>")
            return

        room = game.player.current_room
        target_name = list_of_words[1].lower()

        # Chercher le personnage par nom dans la liste
        target = None
        for char in room.characters:
            if char.name.lower() == target_name:
                target = char
                break

        if not target:
            print(f"{target_name} n'est pas présent ici.")
            return

        target.get_msg()

        objective = f"Parler à {target.name}"
        game.player.quest_manager.complete_objective(objective)

    @staticmethod
    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True


    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True


    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Try to activate the quest
        if game.player.quest_manager.activate_quest(quest_title):
            return True

        msg1 = f"\nImpossible d'activer la quête '{quest_title}'. "
        msg2 = "Vérifiez le nom ou si elle n'est pas déjà active.\n"
        print(msg1 + msg2)
        # print(f"\nImpossible d'activer la quête '{quest_title}'. \
        #             Vérifiez le nom ou si elle n'est pas déjà active.\n")
        return False


    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        """
        Display all rewards earned by the player.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all rewards
        game.player.show_rewards()
        return True
