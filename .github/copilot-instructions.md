# TBA Game - Copilot Instructions

## Project Overview

**TBA** is a text-based adventure game written in French where the player (Lisa) navigates a college campus to find an electronic cigarette. The game features two UI modes: a CLI (command-line) and a Tkinter GUI. The codebase emphasizes modular design with clear separation of concerns across game systems.

**Run with:** `python game.py` (GUI mode) or `python game.py --cli` (CLI mode)

## Architecture & Key Components

### Core Game Loop
- [game.py](game.py): Main orchestrator. `Game` class manages rooms, commands, player, characters, and quests. `GameGUI` (extends `tk.Tk`) wraps the game in a Tkinter GUI with command entry, room display, and directional buttons. Entry point: `main()` function at end of file.
- **Initialization flow:** `Game.setup()` → `setup_commands()`, `setup_commands2()`, `setup_rooms()`, `setup_characters()`, `setup_items()` → `_setup_quests()` → gameplay loop

### World/Navigation Model
- [room.py](room.py): `Room` class holds name, description, inventory of items, characters list, and exits dictionary. Exits map directions (N/S/E/O/U/D) to either adjacent rooms or `(room, Door)` tuples for locked passages. Rooms have optional `image` attribute for GUI and special attributes like `is_shop` or `book_text`.
- [item.py](item.py): `Item` (name, description, weight, price) and `Inventory` container (list of items). Items track weight for inventory limits; shops use `price` field.

### Player & Status
- [player.py](player.py): `Player` class wraps `Inventory`, `Status` (tracks money, rewards, move_count), and `QuestManager`. Player has `current_room`, `history` (visited rooms), and methods for money/reward management. `Status` consolidates player statistics to respect Pylint limits.

### NPC Behavior
- [character.py](character.py): `Character` (non-player entity) with name, description, location, and cycling message list. Characters have their own inventory and can receive/give items.

### Action System
- [command.py](command.py): `Command` class associates a command word (e.g., "go") with a static method from `Actions` class and parameter count.
- [actions.py](actions.py): All player actions as static methods (e.g., `go()`, `take()`, `talk()`, `give()`, `buy()`, `create()`). Validates parameter counts, handles special logic (locked doors, shops, quests). Key pattern: actions check `number_of_parameters` and print error messages if mismatched.

### Quest System
- [quests.py](quests.py): `Quest` class with title, description, objectives (list), status flags (active, completed, reward_given), and rewards. `QuestManager` (in Player) tracks quest lifecycle. Quest rewards can be strings, items, or money dicts.

## Development Patterns & Conventions

### Command Registration
All commands are registered in `Game.setup_commands()` and `Game.setup_commands2()`. Pattern:
```python
cmd = Command("word", " <param> : description", Actions.method, param_count)
self.commands["word"] = cmd
```

### Action Implementation
Each action is a static method in `Actions` class with signature:
```python
@staticmethod
def action_name(game, list_of_words, number_of_parameters):
    # validate: if len(list_of_words) != number_of_parameters + 1: return False
    # access: game.player, game.rooms, game.characters
    return bool  # success/failure
```

### Exit & Door Handling
- Simple exit: `room.exits["N"] = adjacent_room`
- Locked exit: `room.exits["N"] = (adjacent_room, Door(locked=True, key_name="keys"))`
- Player must use `unlock <direction>` with matching key before traversing locked exits.

### French Text
Game content (room descriptions, character messages, item names) is predominantly in French. Maintain consistency; error messages follow pattern: `"\n<content>\n"`

### GUI-Specific Details
- `GameGUI._send_command()` calls `game.process_command()` and updates room image.
- `_StdoutRedirector` redirects all print() output to Tkinter Text widget.
- Direction buttons map to "go N/S/E/O/U/D" commands or special commands like "back", "look".
- Room images in `static/assets/` loaded by name (e.g., "bu.png") on canvas; fallback displays room name.

## Key Files to Reference

| File | Purpose |
|------|---------|
| [game.py](game.py) | Main game class, command setup, room/character/item initialization, game loop, Tkinter GUI |
| [room.py](room.py) | Room abstraction with exits, inventory, character lists |
| [player.py](player.py) | Player state, inventory, quest manager, status tracking |
| [actions.py](actions.py) | All command implementations; check this for interaction patterns |
| [quests.py](quests.py) | Quest definition and manager; reward system |
| [character.py](character.py) | NPC entities with messaging and inventory |

## Important Notes for Agents

1. **French Content:** Comments, docstrings, and game text are in French. Preserve language when modifying.
2. **Inventory Weight System:** Player has `status.max_weight` limit (default 10kg). Actions check total weight before adding items.
3. **Quest State:** Quests transition through active → completed → reward_given. Always check `quest.status["active"]` before unlocking quest content.
4. **Door Key Matching:** Key name in `Door(key_name="X")` must match item name in player inventory for unlock to work.
5. **Special Room Attributes:** Some rooms have `is_shop=True`, `book_text=...`, `image=...`, or `money` fields added dynamically in `setup_items()`.
6. **GUI/CLI Branching:** Code handles both `TKINTER_AVAILABLE` True/False. CLI-only actions still work when --cli flag is used.
7. **Multi-object Commands:** Commands like `give <item> <character>` use index checking: `list_of_words[1]` is first param, `list_of_words[2]` is second.
