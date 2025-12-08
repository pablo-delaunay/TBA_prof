import random

class Character:

    def __init__(self, name, description, current_room=None, msgs=None):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs if msgs is not None else []
        self._msg_index = 0
        self.last_room = current_room


    
    def __str__(self):
        return f"{self.name} : {self.description}"

    def get_msg(self):
        if not self.msgs:
            print(f"{self.name} n'a rien à dire pour l'instant.")
            return
        
        # Affiche le premier message et le supprime de la liste
        message = self.msgs.pop(0)
        print(message)
        
        # Remet le message à la fin de la liste pour le cycle
        self.msgs.append(message)

    import random

    import random

    def move(self):
        # 50% de chance de ne pas bouger
        if random.random() < 0.5:
            return False, self.current_room  # retourne False et la salle actuelle

        # Lister les sorties valides
        exits = [room for room in self.current_room.exits.values() if room is not None]
        if not exits:
            return False, self.current_room

        old_room = self.current_room
        new_room = random.choice(exits)

        # Mettre à jour les rooms
        if self in old_room.characters:
            old_room.characters.remove(self)
        new_room.characters.append(self)
        self.current_room = new_room

        return True, old_room



