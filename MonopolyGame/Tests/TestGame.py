from MonopolyGame.Common import Card
from MonopolyGame.GameTypes import CmdLineGame
from MonopolyGame.Utils.DataClasses import Ring
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
    players = iter(Ring(game.players))
    p = next(players)
    rolled = 0

    while len(game.players) > 1:
        go_next = game.show_menu(p)
        if go_next:
            p = next(players)

    # print("\n".join([str(i) for i in squares]))
