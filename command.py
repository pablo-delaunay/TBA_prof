"""Ce module contient la classe Command."""

class Command:
    """
    This class represents a command. A command is composed of a command word,
    a help string, an action and a number of parameters.

    Attributes:
        command_word (str): The command word.
        help_string (str): The help string.
        action (function): The action to execute when the command is called.
        number_of_parameters (int): The number of parameters expected by the command.

    Methods:
        __init__(self, command_word, help_string, action, number_of_parameters) : The constructor.
        __str__(self) : The string representation of the command.
    """

    def __init__(self, command_word, help_string, action, number_of_parameters):
        """
        Initialise une commande.

        Args :
            command_word (str) : Le mot-clé de la commande.
            help_string (str) : La chaîne d'aide de la commande.
            action (function) : La fonction à exécuter lorsque la commande est appelée.
            number_of_parameters (int) : Le nombre de paramètres attendus.
        """
        self.command_word = command_word
        self.help_string = help_string
        self.action = action
        self.number_of_parameters = number_of_parameters

    def execute(self, game, list_of_words):
        """
        Exécute l'action associée à la commande.

        Args:
            game (Game): L'objet jeu.
            list_of_words (list[str]): Les mots de la commande.
        
        Returns:
            bool: True si l'action s'est exécutée correctement, False sinon.
        """
        return self.action(game, list_of_words, self.number_of_parameters)


    def __str__(self):
        """
        Retourne une représentation lisible de la commande, combinant le mot-clé et l'aide.

        Returns :
            str : La chaîne représentant la commande.
        """
        return  self.command_word \
                + self.help_string
