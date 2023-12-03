# Monopoly

Python implementation of the typical Monopoly game

## Source code

All **interesting** source code is in `MonopolyGame/MonopolyGame`.

### Common - the game itself

* Most code that governs "cards" (such as Chance and Community chest cards) are in `Card.py`
* Most code that governs what different squares do are in `Square.py`
* `Player.py` dictates actions that players can take
* `Game.py` contains code that governs the game state itself.

### GameTypes - different implementations of the "frontend"

* First priority is a command line interface that allows the player to play with all functionality

### Utils - data structures and miscellaneous

* `DataClasses.py` is for dataclasses
  * Future work includes providing a "machine readable" interface that allows AI training (terminal goal #1) and an interface to allow players to play over web (terminal goal #2)
  * Contains a "Ring" buffer
  * Contains the "Result" object, a skeleton for "results", i.e. return types. ~~Not unlikely to be phased out at some point.~~ **Moved into `Utils/Dataclasses.py`
* Utils.py - only contains an importer that serves as a helper function for the Command Line game type right now. Likely will be moved into individual GameTypes at some point.

## Usage

### Command line interface

See `MonopolyGame/Tests/TestGame.py` for an example; run `pip install -e MonopolyGame`, point `Global.importer` to JSON data specifying squares, and add players.

Note that the current implementation is heavily dependent on the user's terminal due to colorful printing.
