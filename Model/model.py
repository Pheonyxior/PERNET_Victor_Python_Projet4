class Match:
    # Un match unique doit être stocké sous la forme d'un tuple contenant deux
    # listes, chacune contenant deux éléments : un joueur et un score.
    data: tuple = [], []


class Turn:
    matchs: list[Match]
    name: str
    start_time: str
    end_time: str


class Player:
    points: int = 0


class Tournament:
    name: str
    place: str
    start_date: str
    end_date: str
    turn_number: int = 4
    current_turn: int = 0
    turns: list[Turn]
    registered_players: list[Player]
    description: str


def test():
    print()
