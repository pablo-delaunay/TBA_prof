"""
Ce module définit la classe Quest, représentant une quête dans le jeu,
ainsi que sa gestion de progression et de récompenses.
"""

from item import Item

class Quest:
    """
    This class represents a quest in the game. A quest has a title, description,
    objectives, completion status, and optional rewards.
    
    Attributes:
        title (str): The title of the quest.
        description (str): The description of the quest.
        objectives (list): List of objectives to complete.
        status (dict): Dictionary containing active, completed, and reward flags.
        reward (str/dict): Optional reward for completing the quest.
    """

    def __init__(self, title, description, objectives=None, reward=None):
        """
        Initialize a new quest.
        
        Args:
            title (str): The title of the quest.
            description (str): The description of the quest.
            objectives (list): List of objectives (default: empty list).
            reward (str/dict): Optional reward description or dictionary.
            
        Examples:
        >>> quest = Quest("Test", "Desc", ["Obj 1"], "Gold")
        >>> quest.is_active
        False
        """
        self.title = title
        self.description = description
        self.objectives = objectives if objectives is not None else []
        self.completed_objectives = []
        self.reward = reward
        # Groupés pour éviter R0902 (Too many instance attributes)
        self.status = {
            "completed": False,
            "active": False,
            "reward_given": False
        }

    @property
    def is_active(self):
        """bool: Whether the quest is currently active."""
        return self.status["active"]

    @is_active.setter
    def is_active(self, value):
        """Sets the active status of the quest."""
        self.status["active"] = value

    @property
    def is_completed(self):
        """bool: Whether the quest is completed."""
        return self.status["completed"]

    @is_completed.setter
    def is_completed(self, value):
        """Sets the completion status of the quest."""
        self.status["completed"] = value

    @property
    def reward_given(self):
        """bool: Whether the reward has already been distributed."""
        return self.status["reward_given"]

    @reward_given.setter
    def reward_given(self, value):
        """Sets the reward_given status."""
        self.status["reward_given"] = value

    def activate(self):
        """
        Activate the quest.
        
        Examples:
        >>> quest = Quest("Adventure", "Go on an adventure")
        >>> quest.activate()
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Adventure
        📝 Go on an adventure
        <BLANKLINE>
        """
        self.is_active = True
        print(f"\n🗡️  Nouvelle quête activée: {self.title}")
        print(f"📝 {self.description}\n")

    def complete_objective(self, objective, player=None):
        """
        Mark an objective as completed.
        
        Args:
            objective (str): The objective to mark as completed.
            player: The player object (optional).
            
        Returns:
            bool: True if objective was found and completed, False otherwise.
        """
        if objective in self.objectives and objective not in self.completed_objectives:
            self.completed_objectives.append(objective)

            if len(self.completed_objectives) == len(self.objectives):
                self.complete_quest(player)
            print(f"✅ Objectif accompli: {objective}")
            return True
        return False

    def complete_quest(self, player=None):
        """
        Mark the quest as completed and give reward to player.
        
        Args:
            player: The player object to give the reward to (optional).
        """
        if not self.is_completed:
            self.is_completed = True
            if self.reward and player:
                # Note: La logique de distribution est gérée par le QuestManager
                # mais nous gardons la compatibilité ici.
                pass
            print()

    def get_status(self):
        """
        Get the current status of the quest.
        
        Returns:
            str: A formatted string showing the quest status.
        """
        if not self.is_active:
            return f"❓ {self.title} (Non activée)"
        if self.is_completed:
            return f"✅ {self.title} (Terminée)"

        completed_count = len(self.completed_objectives)
        total_count = len(self.objectives)
        return f"⏳ {self.title} ({completed_count}/{total_count} objectifs)"

    def __str__(self):
        """Return a string representation of the quest."""
        return self.get_status()

class QuestManager:
    """
    This class manages all quests in the game.
    
    Attributes:
        quests (list): List of all quests in the game.
        active_quests (list): List of currently active quests.
        player: Reference to the player object.
    """


    def __init__(self, player=None, game=None):
        """
        Initialize the quest manager.
        
        Args:
            player: The player object (optional, can be set later).
            
        Examples:
        
        >>> manager = QuestManager()
        >>> len(manager.quests)
        0
        >>> len(manager.active_quests)
        0
        """
        self.quests = []
        self.active_quests = []
        self.player = player
        self.game = game  # Initialize game here


    def add_quest(self, quest):
        """
        Add a quest to the game.
        
        Args:
            quest (Quest): The quest to add.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest = Quest("Quest 1", "First quest")
        >>> manager.add_quest(quest)
        >>> len(manager.quests)
        1
        >>> manager.quests[0].title
        'Quest 1'
        """
        self.quests.append(quest)


    def activate_quest(self, quest_title):
        """
        Activate a quest by its title.
        
        Args:
            quest_title (str): The title of the quest to activate.
            
        Returns:
            bool: True if quest was found and activated, False otherwise.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest = Quest("Epic Quest", "An epic adventure")
        >>> manager.add_quest(quest)
        >>> manager.activate_quest("Epic Quest")
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Epic Quest
        📝 An epic adventure
        <BLANKLINE>
        True
        >>> len(manager.active_quests)
        1
        >>> manager.activate_quest("Unknown Quest")
        False
        """
        for quest in self.quests:
            if quest.title == quest_title and not quest.is_active:
                quest.activate()
                self.active_quests.append(quest)
                return True
        return False


    def complete_objective(self, objective_text):
        """
        Complete an objective in any active quest.
        
        Args:
            objective_text (str): The objective to complete.
            
        Returns:
            bool: True if objective was found and completed, False otherwise.
        """
        for quest in self.active_quests:
            if quest.complete_objective(objective_text):

                if quest.is_completed and not quest.reward_given:
                    quest.reward_given = True

                    print(f"\n🏆 Quête terminée: {quest.title}")

                    reward = quest.reward

                    # recevoir de l'argent
                    if quest.title == "Mission Pablo":
                        self.player.money += 10
                        print("💰 Vous recevez 10€ de la part de Pablo.")

                    # recevoir un objet
                    elif reward["type"] == "item":
                        item = Item(
                            reward["name"],
                            description=f"Récompense de la quête '{quest.title}'",
                            weight=reward["weight"]
                        )
                        self.player.inventory.add_item(item)
                        print(f"🎁 Vous recevez : {item.name}")

                    # fin du jeu
                    elif reward and reward.get("type") == "finish_game":
                        print("\n🎉 Félicitations ! Vous avez aidé Lisa à trouver sa cigarette "\
                              "électronique et terminé le jeu ! 🎉\n")
                        if self.game:
                            self.game.finished = True
        return False




    def check_room_objectives(self, room_name):
        """
        Check all active quests for room-related objectives.
        
        Args:
            room_name (str): The name of the room visited.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest = Quest("Visit Places", "Visit rooms", ["Visiter Library"])
        >>> manager.add_quest(quest)
        >>> manager.activate_quest("Visit Places") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Visit Places
        📝 Visit rooms
        <BLANKLINE>
        True
        >>> manager.check_room_objectives("Library") # doctest: +NORMALIZE_WHITESPACE
        ✅ Objectif accompli: Visiter Library
        <BLANKLINE>
        🏆 Quête terminée: Visit Places
        <BLANKLINE>
        >>> len(manager.active_quests)
        0
        """
        for quest in self.active_quests[:]:  # Use slice to avoid modification during iteration
            quest.check_room_objective(room_name, self.player)
            if quest.is_completed:
                self.active_quests.remove(quest)


    def check_action_objectives(self, action, target=None):
        """
        Check all active quests for action-related objectives.
        
        Args:
            action (str): The action performed.
            target (str): Optional target of the action.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest = Quest("Actions", "Do actions", ["parler avec roi"])
        >>> manager.add_quest(quest)
        >>> manager.activate_quest("Actions") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Actions
        📝 Do actions
        <BLANKLINE>
        True
        >>> manager.check_action_objectives("parler", "roi") # doctest: +NORMALIZE_WHITESPACE
        ✅ Objectif accompli: parler avec roi
        <BLANKLINE>
        🏆 Quête terminée: Actions
        <BLANKLINE>
        >>> len(manager.active_quests)
        0
        """
        for quest in self.active_quests[:]:
            quest.check_action_objective(action, target, self.player)
            if quest.is_completed:
                self.active_quests.remove(quest)


    def check_counter_objectives(self, counter_name, current_count):
        """
        Check all active quests for counter-related objectives.
        
        Args:
            counter_name (str): The name of what is being counted.
            current_count (int): The current count.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest = Quest("Counter", "Count things", ["Compter 3 fois"])
        >>> manager.add_quest(quest)
        >>> manager.activate_quest("Counter") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Counter
        📝 Count things
        <BLANKLINE>
        True
        >>> manager.check_counter_objectives("Compter", 2)
        >>> len(manager.active_quests)
        1
        >>> manager.check_counter_objectives("Compter", 3) # doctest: +NORMALIZE_WHITESPACE
        ✅ Objectif accompli: Compter 3 fois
        <BLANKLINE>
        🏆 Quête terminée: Counter
        <BLANKLINE>
        >>> len(manager.active_quests)
        0
        """
        for quest in self.active_quests[:]:
            quest.check_counter_objective(counter_name, current_count, self.player)
            if quest.is_completed:
                self.active_quests.remove(quest)


    def get_active_quests(self):
        """
        Get all active quests.
        
        Returns:
            list: List of active quests.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest = Quest("Active Quest", "An active quest")
        >>> manager.add_quest(quest)
        >>> len(manager.get_active_quests())
        0
        >>> manager.activate_quest("Active Quest")
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Active Quest
        📝 An active quest
        <BLANKLINE>
        True
        >>> len(manager.get_active_quests())
        1
        """
        return self.active_quests


    def get_all_quests(self):
        """
        Get all quests.
        
        Returns:
            list: List of all quests.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest1 = Quest("Q1", "First")
        >>> quest2 = Quest("Q2", "Second")
        >>> manager.add_quest(quest1)
        >>> manager.add_quest(quest2)
        >>> len(manager.get_all_quests())
        2
        """
        return self.quests


    def get_quest_by_title(self, title):
        """
        Get a quest by its title.
        
        Args:
            title (str): The title of the quest.
            
        Returns:
            Quest: The quest if found, None otherwise.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest1 = Quest("Find Key", "Find the golden key")
        >>> quest2 = Quest("Open Door", "Open the locked door")
        >>> manager.add_quest(quest1)
        >>> manager.add_quest(quest2)
        >>> found = manager.get_quest_by_title("Find Key")
        >>> found.title
        'Find Key'
        >>> manager.get_quest_by_title("Unknown") is None
        True
        """
        for quest in self.quests:
            if quest.title == title:
                return quest
        return None


    def show_quests(self):
        """
        Display all quests and their status.
        
        Examples:
        
        >>> manager = QuestManager()
        >>> manager.show_quests()
        <BLANKLINE>
        Aucune quête disponible.
        <BLANKLINE>
        >>> quest = Quest("Display Quest", "Test display")
        >>> manager.add_quest(quest)
        >>> manager.show_quests() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        📋 Liste des quêtes:
        ❓ Display Quest (Non activée)
        <BLANKLINE>
        """
        if not self.quests:
            print("\nAucune quête disponible.\n")
            return

        print("\n📋 Liste des quêtes:")
        for quest in self.quests:
            print(f"  {quest.get_status()}")
        print()


    def show_quest_details(self, quest_title, current_counts=None):
        """
        Show detailed information about a specific quest.
        
        Args:
            quest_title (str): The title of the quest.
            current_counts (dict): Optional dictionary with current counter values.
            
        Examples:
        
        >>> manager = QuestManager()
        >>> quest = Quest("Detail Quest", "Show details", ["Task"])
        >>> manager.add_quest(quest)
        >>> manager.show_quest_details("Detail Quest") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        📋 Quête: Detail Quest
        📖 Show details
        <BLANKLINE>
        Objectifs:
        ⬜ Task
        <BLANKLINE>
        >>> manager.show_quest_details("Unknown")
        <BLANKLINE>
        Quête 'Unknown' non trouvée.
        <BLANKLINE>
        """
        quest = self.get_quest_by_title(quest_title)
        if quest:
            print(quest.get_details(current_counts))
        else:
            print(f"\nQuête '{quest_title}' non trouvée.\n")
