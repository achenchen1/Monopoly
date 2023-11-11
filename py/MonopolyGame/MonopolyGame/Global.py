from Result import Result

chance_cards = []
houses = 0
hotels = 0


class GlobalError(Result):
    pass


class NoMoreHouses(GlobalError):
    default_message = "No more houses left in the game."


class NoMoreHotels(GlobalError):
    default_message = "No more hotels left in the game."
