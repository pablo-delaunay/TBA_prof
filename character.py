"""
Module character.

Contient la classe Character représentant un personnage non-joueur (PNJ)
dans le jeu, avec ses messages et son déplacement aléatoire.
"""
import random

class Character:
    """
    Cette classe représente un personnage non-joueur (PNJ) dans le jeu.

    Un personnage possède un nom, une description, une salle actuelle, une liste de messages
    qu'il peut dire et peut se déplacer aléatoirement vers des salles adjacentes.

    Attributs:
        name (str): Le nom du personnage.
        description (str): La description du personnage.
        current_room (Room | None): La salle où se trouve actuellement le personnage.
        msgs (list[str]): La liste des messages que le personnage peut dire.
        _msg_index (int): Index interne utilisé pour le cycle des messages.
        last_room (Room | None): La dernière salle visitée par le personnage.

    Méthodes:
        __init__(self, name, description, current_room=None, msgs=None) : Initialise le personnage.
        __str__(self) : Retourne une représentation textuelle du personnage.
        get_msg(self) : Affiche un message du personnage.
        move(self) : Déplace le personnage aléatoirement vers une salle adjacente si possible.
    """

    def __init__(self, name, description, current_room=None, msgs=None):
        """
        Initialise un personnage.

        Args:
            name (str): Nom du personnage.
            description (str): Description du personnage.
            current_room (Room | None, optional): Salle actuelle du personnage.
            msgs (list[str], optional): Liste de messages du personnage.
        """
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs if msgs is not None else []
        self._msg_index = 0
        self.last_room = current_room

    def __str__(self):
        """
        Retourne une représentation lisible du personnage.

        Returns:
            str: Nom et description du personnage.
        """
        return f"{self.name} : {self.description}"

    def get_msg(self):
        """
        Affiche un message du personnage.

        Le message est affiché et remis à la fin de la liste pour permettre un cycle.
        Si le personnage n'a aucun message, un avertissement est affiché.
        """
        if not self.msgs:
            print(f"{self.name} n'a rien à dire pour l'instant.")
            return

        message = self.msgs.pop(0)
        print(message)

        self.msgs.append(message)


    def move(self):
        """
        Déplace le personnage aléatoirement vers une salle voisine.

        La probabilité de se déplacer est de 50%. Le personnage ne traverse
        que les portes ouvertes.

        Returns:
            tuple:
                bool: True si le personnage a changé de salle, False sinon.
                Room: Ancienne salle avant le déplacement.
        """
        if random.random() < 0.5:
            return False, self.current_room

        exits = []

        for exit_info in self.current_room.exits.values():
            if exit_info is None:
                continue

            # Si c'est une porte : (room, door)
            if isinstance(exit_info, tuple):
                room, door = exit_info
                if not door.locked:  # le personnage ne traverse que si ouvert
                    exits.append(room)
            else:
                exits.append(exit_info)

        if not exits:
            return False, self.current_room

        old_room = self.current_room
        new_room = random.choice(exits)

        # Mise à jour des salles
        if self in old_room.characters:
            old_room.characters.remove(self)

        new_room.characters.append(self)
        self.current_room = new_room

        return True, old_room
