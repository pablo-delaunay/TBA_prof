" Actions for the game commands."


from item import Item


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

        direction = list_of_words[1].upper()

                # ⚠️ Avertissement Crackheads depuis le Chemin
        if player.current_room == game.rooms["Chemin"] and direction == "O":
            print("Titouan : Lisa il y a des crackheads là-bas "\
                  "c'est dangereux, tu es sûre d'y aller ?")
            answer = game.get_input("(oui/non) > ").lower().strip()
            if answer == "oui":
                print("\nLisa est morte tuée.")
                game.finished = True
                return False
            else:
                print("\nTu restes dans le chemin.")
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

        # Affichage de l'historique
        hist = player.get_history()
        if hist:
            print(hist)

        # Affichage
        print(next_room.get_long_description())
        if getattr(next_room, "is_shop", False):
            print("\n🛒 Le magasin propose :")
            for item in next_room.inventory.items:
                print(f" - {item.name} ({item.price}€)")

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
        if door.locked:
            print("\n🚪 La porte est verrouillée. Utilisez 'unlock <direction>'.\n")
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

        # Afficher l'historique et la description
        hist = player.get_history()
        if hist != "":
            print(hist)
        print(player.current_room.get_long_description())

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
        room = game.player.current_room


        # Argent au sol
        money = getattr(room, "money", 0)
        if money > 0:
            print(f"💰 Vous trouvez {money}€ par terre.")
            game.player.money += money
            room.money = 0

        # Livre dans la BU
        if room.name.lower() == "bu":
            print("📘 Un livre est posé sur une table. (read livre)")

        # Inventaire de la pièce
        if getattr(room, "is_shop", False):
            print("🛒 Des objets sont en vente ici. Utilisez `buy <objet>`.")
        else:
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

        if found.name.lower() == "chien":
            game.player.quest_manager.complete_objective("Prendre le chien")

        if found.name.lower() == "base":
            game.player.quest_manager.complete_objective("Avoir une base dans l'inventaire")

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
        if room.name.lower() == "parc" and item.name.lower() == "chien":
            game.player.quest_manager.complete_objective("Ramener le chien au parc")


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

        _, door = exit_info

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

        if target.name == "Pablo":
            game.player.quest_manager.activate_quest("Mission Pablo")

        objective = f"Parler à {target.name}"
        game.player.quest_manager.complete_objective(objective)
        print(target.inventory.get_inventory(f"{target.name} possède :"))

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
    def give(game, list_of_words, _number_of_parameters):
        """
        Permet au joueur de donner un objet à un personnage dans la salle.

        Args:
            game (Game): L'objet jeu.
            list_of_words (list[str]): La commande, le nom de l'objet et le nom du personnage.
            _number_of_parameters (int): Non utilisé.

        Returns:
            None
        """
        if len(list_of_words) != 3:
            print("Utilisation : give <nom de l'objet> <nom du personnage>")
            return

        item_name = list_of_words[1].lower()
        target_name = list_of_words[2].lower()
        player = game.player
        room = player.current_room

        # Vérifier si l'objet est dans l'inventaire du joueur
        item = player.inventory.remove_item(item_name)
        if item is None:
            print(f"\nVous ne possédez pas l'objet '{item_name}'.\n")
            return

        # Chercher le personnage par nom dans la salle
        target = None
        for char in room.characters:
            if char.name.lower() == target_name:
                target = char
                break

        if not target:
            print(f"{target_name} n'est pas présent ici.")
            # Remettre l'objet dans l'inventaire du joueur
            player.inventory.add_item(item)
            return

        # Donner l'objet au personnage
        print(f"\nVous donnez '{item.name}' à {target.name}.\n")
        target.receive_item(item)

        if item.name.lower() == "cookie" and target.name.lower() == "pablo":
            game.player.quest_manager.complete_objective("Ramener le cookie à Pablo")


    @staticmethod
    def ask(game, words, num_params):
        item_name = words[1].lower()      # normalisation
        target_name = words[2].lower()

        # trouver le personnage
        target = None
        for character in game.characters:
            if character.name.lower() == target_name:
                target = character
                break
        if not target:
            print(f"{target_name} n'est pas là.")
            return

        # vérifier si l'objet existe dans l'inventaire du personnage
        item = target.inventory.get_item(item_name)  # <-- récupère l'objet Item
        if not item:
            print(f"{target.name} n'a pas pu vous donner '{item_name}'.")
            return

        # retirer l'objet du personnage
        target.inventory.remove_item(item.name)
        # ajouter l'objet réel à l'inventaire du joueur
        game.player.inventory.add_item(item)
        print(f"Vous avez reçu '{item.name}' de {target.name}.")

        if item.name.lower() == "ce":
            game.player.quest_manager.complete_objective("Avoir une CE dans l'inventaire")

    @staticmethod
    def read(game, words, _num_params):
        if len(words) != 2:
            print("Utilisation : read <objet>")
            return

        target = words[1].lower()
        room = game.player.current_room

        # 📖 lecture du livre dans la BU
        if target == "livre" and hasattr(room, "book_text"):
            print("\n" + room.book_text + "\n")
            return

        print("Il n'y a rien à lire ici.")


    def move(self, direction):
        """
        Déplace le joueur vers une salle voisine.

        Args:
            direction (str): La direction du déplacement (ex: 'N', 'E', ...).

        Returns:
            bool: True si le déplacement est réussi, False sinon.
        """
        next_room = self.current_room.exits.get(direction)

        if next_room is None:
            # Message personnalisé si défini dans la salle
            if direction in self.current_room.fail_messages:
                print("\n" + self.current_room.fail_messages[direction] + "\n")
            else:
                print("\nImpossible d'aller dans cette direction.\n")
            return False

        # Mise à jour de la salle actuelle et de l'historique
        self.current_room = next_room
        self.history.append(self.current_room)

        # Affichage de l'historique
        hist = self.get_history()
        if hist:
            print(hist)

        print(self.current_room.get_long_description())

        # Incrément du compteur de déplacements
        self.status.move_count += 1

        return True



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

    @staticmethod
    def money(game, list_of_words, number_of_parameters):
        if len(list_of_words) != 1:
            print("Utilisation : money")
            return False

        game.player.show_money()
        return True


    @staticmethod
    def buy(game, list_of_words, _):
        room = game.player.current_room

        if room.name.lower() != "magasin":
            print("❌ Vous devez être au magasin pour acheter.")
            return

        item_name = list_of_words[1]
        item = room.inventory.get_item(item_name)

        if item is None:
            print("❌ Cet objet n'est pas en vente.")
            return

        if game.player.money < item.price:
            print("❌ Vous n'avez pas assez d'argent.")
            return

        # Achat
        game.player.money -= item.price
        room.inventory.remove_item(item_name)
        game.player.inventory.add_item(item)

        print(f"🛒 Vous achetez {item.name} pour {item.price}€.")

        if item.name.lower() == "résistance":
            game.player.quest_manager.complete_objective(
                "Avoir une résistance dans l'inventaire"
                )
        if item.name.lower() == "cerise":
            game.player.quest_manager.complete_objective(
                "Avoir des cerises dans l'inventaire"
                )



    @staticmethod
    def sell(game, list_of_words, _number_of_parameters):
        player = game.player
        room = player.current_room

        if room.name.lower() != "magasin":
            print("\nVous devez être dans le magasin pour vendre.\n")
            return

        item_name = list_of_words[1].lower()
        item = player.inventory.get_item(item_name)

        if not item:
            print(f"\nVous ne possédez pas '{item_name}'.\n")
            return

        sell_price = item.price // 2

        player.inventory.remove_item(item_name)
        room.inventory.add_item(item)
        player.money += sell_price

        print(f"\n💰 Vous vendez '{item.name}' pour {sell_price}€.\n")


    def create(game, list_of_words, number_of_parameters):
        """
        Crée un 'gout' si le joueur est au Crous et possède l'ingrédient.
        La commande doit être exactement : create gout
        """

        # Vérifier que le joueur a bien tapé 2 mots : create + gout
        if len(list_of_words) != 2 or list_of_words[1].lower() != "gout":
            print("❌ Commande invalide. Tapez : create gout")
            return False

        # Vérifier la salle
        if game.player.current_room != game.rooms["Crous"]:
            print("❌ Vous devez être au Crous pour créer un gout.")
            return False

        # Vérifier l'ingrédient
        if not game.player.inventory.has_item("base"):
            print("❌ Il vous faut une base et des cerises pour créer un gout.")
            return False

        if not game.player.inventory.has_item("cerise"):
            print("❌ Il vous faut une cerise et une base pour créer un gout.")
            return False

        # Empêcher doublon
        if game.player.inventory.has_item("gout"):
            print("❌ Vous avez déjà un gout.")
            return False

        # Consommer l'ingrédient
        game.player.inventory.remove_item("base")
        game.player.inventory.remove_item("cerise")


        # Créer le gout
        item = Item(
            name="gout",
            description="Un délicieux gout fait maison",
            weight=0.005,
            price=0
        )

        game.player.inventory.add_item(item)

        # Objectifs de quête
        game.player.quest_manager.complete_objective("Créer un gout")

        return True
