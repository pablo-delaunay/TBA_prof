class Item:
    def __init__(self,name, description, weight):
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item_name):
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
            return item
        return None

    def get_inventory(self, prefix_message="Vous disposez des items suivants :"):
        if not self.items:
            return "Il n'y a rien ici." if prefix_message.startswith('La pièce') else "Vous ne disposez d'aucun item."
        inv = f"{prefix_message}\n"
        for item in self.items:
            inv += f" - {item}\n"
        return inv
