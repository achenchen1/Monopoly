from MonopolyGame import Card, Global
from MonopolyGame.Global import importer

if __name__ == "__main__":
    squares = []
    chance = [Card.GoToGo("Advance to GO", "(Collect $200)")]
    community_chest = [Card.GoToGo("Advance to GO", "(Collect $200)")]
    game = Global.Game(squares, chance, community_chest)
    importer(
        "/Users/alexchen/Projects/Monopoly/resources/squares.json",
        squares,
        chance,
        community_chest,
        game,
    )
    player = game.add_player(0, (33, 150, 243))
    player = game.add_player(1, (226, 50, 107))
    while len(game.players) > 1:
        for p in game.players:
            game.show_menu(p)
    # print("\n".join([str(i) for i in squares]))
