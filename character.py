class Character:

    def __init__(self, name, description, current_room=None, msgs=None):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs if msgs is not None else []
        self._msg_index = 0

    
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

