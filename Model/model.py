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
    def __init__(self, surname, name, date_of_birth, chess_id):
        self.surname = surname
        self.name = name
        self.date_of_birth = date_of_birth
        self.chess_id = chess_id


class Tournament:
    current_turn: int = 0
    turns: list[Turn] = []
    registered_players: list[Player] = []

    def __init__(self, name, place, start_date, end_date,
                 turn_number=4, description=""):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.turn_number = turn_number
        self.description = description

    def register_player(self, player: Player):
        self.registered_players.append(player)
