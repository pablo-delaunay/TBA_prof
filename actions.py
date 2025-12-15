# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def go(game, list_of_words, number_of_parameters):
        player = game.player

        # Vérifie le nombre de paramètres
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        direction = list_of_words[1].upper()
        synonyms = {
            "N": "N", "NORD": "N",
            "E": "E", "EST": "E",
            "S": "S", "SUD": "S",
            "O": "O", "OUEST": "O",
            "U": "U", "UP": "U",
            "D": "D", "DOWN": "D"
        }

        if direction in synonyms:
            direction = synonyms[direction]
        else:
            print("\nDirection inconnue. Utilisez N, E, S, O, U, D.\n")
            return False

        # 💡 Ici on récupère correctement la room actuelle
        room = player.current_room

        # Récupère la sortie
        exit_info = room.get_exit(direction)

        if exit_info is None:
            print("\nImpossible d'aller dans cette direction.\n")
            return False

        if isinstance(exit_info, tuple):
            next_room, door = exit_info

            # 🔥 Condition EXCLUSIVE : uniquement Rue -> Esiee (direction Nord)
            if game.player.current_room.name == "Rue" and direction == "N":

                if door.locked:
                    # Vérifier si le joueur possède la carte
                    if game.player.inventory.has_item("carte"):
                        door.locked = False
                        print("\nVotre carte étudiante vous permet d'entrer dans l'Esiee.\n")
                    else:
                        print("\nVous ne pouvez pas entrer à l'Esiee sans votre carte étudiante.\n")
                        return False

            # Pour toutes les autres portes éventuelles : porte ignorée (considérée ouverte)
            # Donc : aucune autre porte n'est bloquée par une clé.

        else:
            next_room = exit_info

        # Déplacement du joueur
        player.current_room = next_room
        player.history.append(next_room)

        print(next_room.get_long_description())
        hist = player.get_history()
        if hist != "":
            print(hist)

        for char in game.characters:
            moved, old_room = char.move()
            if moved and old_room == player.current_room:
                print(f"{char.name} s'est déplacé.")

        return True

    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

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
    
    def back(game, list_of_words, number_of_parameters):
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

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

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

    def look(game, list_of_words, number_of_parameters):
        room = game.player.current_room
        # Affiche la description longue de la salle
        print(room.get_long_description())
        # Affiche les items présents dans la salle
        print(room.get_inventory())


    
    def take(game, list_of_words, number_of_parameters):

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
        if player.get_total_weight() + found.weight > player.max_weight:
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


    
    def drop(game, list_of_words, number_of_parameters):

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

    
    def check(game, list_of_words, number_of_parameters):

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

    def unlock(game, list_of_words, number_of_parameters):

        if len(list_of_words) != 2:
            print("Utilisation : unlock <direction>")
            return

        direction = list_of_words[1]
        room = game.player.current_room

        exit_info = room.get_exit(direction)

        if exit_info is None or not isinstance(exit_info, tuple):
            print("Il n'y a pas de porte dans cette direction.")
            return

        next_room, door = exit_info

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

    def talk(game, list_of_words, number_of_parameters):
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

