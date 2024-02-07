from MonopolyGame.Common import Card, Game, Square
from MonopolyGame.GameTypes import CmdLineGame
from MonopolyGame.Utils.DataClasses import Ring, Error
from MonopolyGame.Utils.Utils import importer

if __name__ == "__main__":
    squares = []
    chance = [Card.GoToGo("Advance to GO", "(Collect $200)")]
    community_chest = [Card.GoToGo("Advance to GO", "(Collect $200)")]
    game = CmdLineGame.CmdLineGame(squares, chance, community_chest)
    importer(
        "/Users/alexchen/Projects/Monopoly/resources/squares.json",
        squares,
        chance,
        community_chest,
        game,
    )
    game.update_square_colors()
    game.add_players(2)
    # for square in game.squares:
    #     if issubclass(type(square), Square.Buyable):
    #         game.players[0].properties.append(square)
    #     square.owner = game.players[0]
    # game.players[1].balance = 0
    players = iter(Ring(game.players))
    p = next(players)
    rolled = False

    while len(game.players) > 1:
        result = game.show_menu(p, rolled)
        if isinstance(result, Game.TurnOver):
            p = next(players)
            rolled = False
        elif isinstance(result, Game.Rolled):
            rolled = True
        elif isinstance(result, Error):
            print("Error:", result)
        else:
            print(result)

    # print("\n".join([str(i) for i in squares]))
