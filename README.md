# Monopoly

Python implementation of the typical Monopoly game

## Source code

All **interesting** source code is in `MonopolyGame/MonopolyGame`.

* Most code that governs "cards" (such as Chance and Community chest cards) are in `Card.py`
* Most code that governs what different squares do are in `Square.py`
* `Player.py` dictates actions that players can take
* `Utils.py` is for dataclasses and specific "interfaces"
  * First priority is a command line interface that allows the player to play with all functionality
  * Future work includes providing a "machine readable" interface that allows AI training (terminal goal #1) and an interface to allow players to play over web (terminal goal #2)
* `Result.py` contains a skeleton for "results", i.e. return types. _Not unlikely to be phased out at some point._
* `Global.py` contains code that governs the game state itself.

## Usage

### Command line interface

See `MonopolyGame/Tests/TestGame.py` for an example; run `pip install -e MonopolyGame`, point `Global.importer` to JSON data specifying squares, and add players.

Note that the current implementation is heavily dependent on the user's terminal due to colorful printing.
