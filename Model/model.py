from random import shuffle
import random


class Match:
    # Un match unique doit être stocké sous la forme d'un tuple contenant deux
    # listes, chacune contenant deux éléments : un joueur et un score.
    data: tuple = [], []


class Turn:
    def __init__(self, name, start_time, end_time="0:0", matchs=[]):
        self.name = name
        self.start_time = start_time
        self.matchs = matchs
        self.end_time = end_time


class Player:
    def __init__(self, surname, name, date_of_birth, chess_id):
        self.surname = surname
        self.name = name
        self.date_of_birth = date_of_birth
        self.chess_id = chess_id


class Tournament:
    class PlayerData:
        def __init__(self, id):
            self.id = id
            self.score = 0.0
            self.played_with = []

    def __init__(self, name, place, start_date, end_date, registered_players=[],
                 turns=[], turn_number=4, description=""):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.registered_players = registered_players
        self.turns: list[Turn] = []
        for dic in turns:
            turn = Turn(dic["name"], dic["start_time"], dic["end_time"], dic["matchs"])
            self.turns.append(turn)

        self.current_turn = len(turns)
        self.turn_number = turn_number
        self.description = description

        self.players = {}
        for player in registered_players:
            self.players[player] = self.PlayerData(player)

        for turn in self.turns:
            for match in turn.matchs:
                for result in match:
                    self.players[result[0]].score += result[1]

    def sorted_player_ids(self, reverse=False):
        new_list = list(self.players.values())
        shuffle(new_list)
        new_list.sort(key=lambda player: player.score, reverse=reverse)
        player_ids = []
        for player in new_list:
            player_ids.append(player.id)
        return player_ids

    def make_pairs(self, player_ids: list):
        # associer par paires les joueurs dans l'ordre j1 avec j2 ect
        # si j1 a déjà joué contre j2 associer avec j3
        pairs = []
        players = player_ids.copy()
        pairs_valid = True

        # Regarder si les paires sont valides
        for i in range(0, len(players), 2):
            p1 = players[i]
            p2 = players[i+1]
            if p2 in self.played_with(p1):
                # print(colored(f"{p1} and {p2} already played", 'cyan'))
                pairs_valid = False
                break
            else:
                pairs.append((p1, p2))
                # print(colored((p1,p2), 'green'))

        # Si une erreur dans les paires:
        if not pairs_valid:
            # print(colored("Sorting best pairs", 'cyan'))
            pairs = self.sort_best_pairs(players)

        # mettre à jour la liste des joueurs joués avec
        for pair in pairs:
            p1 = pair[0]
            p2 = pair[1]
            self.players[p1].played_with.append(p2)
            self.players[p2].played_with.append(p1)

        return pairs

    def sort_best_pairs(self, players: list):
        pairs = []
        best_dict = {}
        # Générer un dict de listes dont les clés sont les joueurs ordonnés par leur score croissant
        # chaque liste contient chaque chaque joueur n'ayant pas joué avec le joueur correspondant
        # la liste est ordonné du joueur le plus "proche" en terme de place dans la liste initiale au plus éloigné

        for player in players:
            # générer la liste des joueurs les plus proches
            best_dict[player] = self.get_closest_players(player, players)

        # Prendre la première paire à la fin du dic
        pair = self.get_pair_from_dict(best_dict, players[-1])
        if pair is False:
            pair = self.get_next_best_pair(players, players[-1], best_dict)
        pairs.append(pair)
        # print_dict(best_dict)

        # Pairer le joueur ayant le moins d'adversaires possible tant que le dict n'est pas vide
        while best_dict:
            least_player = min(best_dict, key=lambda x: len(best_dict[x]))
            pair = self.get_pair_from_dict(best_dict, least_player)

            # Cas exceptionnel: si le joueur donné n'a plus aucun adversaire disponible
            if pair is False:
                pair = self.get_next_best_pair(players, least_player, best_dict)

            pairs.append(pair)
            # print_dict(best_dict)

        return pairs

    def get_pair_from_dict(self, d: dict, player_id):
        # pairer la clé du dict (p1) avec le premier joueur de la liste de p1
        # Supprimer les clés de la paire ainsi que leur instances des les listes restantes
        p1 = player_id
        if len(d[p1]) == 0:
            # print(colored(f"{p1} had no available opponent", 'red'))
            return False

        p2 = d.pop(p1)[0]
        # print(colored(f"{p1}, {p2} \n", 'green'))
        d.pop(p2)
        pair = (p1, p2)

        for key in d.keys():
            l: list = d[key]
            new_l = []
            # print(colored(key, 'yellow'))
            for p in l:
                # print(colored(f"p: {p}", 'blue'))
                if p == p1 or p == p2:
                    pass
                    # print(colored(f"removing: {p}", 'red'))
                else:
                    new_l.append(p)
            d[key] = new_l

        return pair

    def get_next_best_pair(self, player_ids: list, least_player, best_dict: dict):
        index = player_ids.index(least_player)
        j = index+1
        h = index-1
        p1 = least_player
        p2 = None
        over = False
        while not over:
            jb = j == len(player_ids)
            hb = h == -1
            if not jb:
                pj = player_ids[j]
                if pj in best_dict.keys():
                    p2 = pj
                    over = True
                j += 1
            if not hb or over:
                ph = player_ids[h]
                if ph in best_dict.keys():
                    p2 = ph
                    over = True
                h -= 1
        pair = (p1, p2)
        # print(colored(f"Exceptionnaly pairing {p1} and {p2}", 'red'))
        best_dict.pop(p1)
        best_dict.pop(p2)
        for key in best_dict.keys():
            l: list = best_dict[key]
            new_l = []
            # print(colored(key, 'yellow'))
            for p in l:
                # print(colored(f"p: {p}", 'blue'))
                if p == p1 or p == p2:
                    pass
                    # print(colored(f"removing: {p}", 'red'))
                else:
                    new_l.append(p)
            best_dict[key] = new_l

        return pair

    def get_closest_players(self, player, players):
        # générer la liste des joueurs les plus proches
        new_list = []
        index = players.index(player)
        over = False
        j = index + 1
        h = index - 1
        p_with = self.played_with(player)

        while not over:
            jb = j == len(players)
            hb = h == -1

            if not jb:
                pj = players[j]
                if pj not in p_with:
                    new_list.append(pj)
                j += 1
            if not hb:
                ph = players[h]
                if ph not in p_with:
                    new_list.append(ph)
                h -= 1
            if jb and hb:
                over = True

        return new_list

    def played_with(self, player_id):
        return self.players[player_id].played_with

    def generate_rand_matchs(self, pairs):
        matchs = []
        for pair in pairs:
            p0_score = 0
            p1_score = 0
            r = random.randint(0, 2)
            match r:
                case 0:
                    p0_score = 0.5
                    p1_score = 0.5
                case 1:
                    p0_score = 1
                    p1_score = -1
                case 2:
                    p0_score = -1
                    p1_score = 1

            # Un match unique doit être stocké sous la forme d'un tuple contenant deux
            # listes, chacune contenant deux éléments : un joueur et un score.
            matchs.append(([pair[0], p0_score], [pair[1], p1_score]))
        return matchs

    def update_players_score(self, matchs):
        for match in matchs:
            self.players[match[0][0]].score += match[0][1]
            self.players[match[1][0]].score += match[1][1]
