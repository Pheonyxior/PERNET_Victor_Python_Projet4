import random
from model import model

# proto module
from termcolor import colored
import time

# tournament = model.Tournament("Tournament", "Place", "0:0", "10:0",
#                              ["Aurore", "Bilbo", "Charlotte", "Dianes", 
#                               "Ekko", "Fleur", "Gaston", "Hanz"])

tournament = model.Tournament("Tournament", "Place", "0:0", "10:0",
                             ["Aurore", "Bilbo", "Charlotte", "Dianes"])
                            #   "Ekko", "Fleur", "Gaston", "Hanz",#
                            #   "Ingrid", "Jean", "Katarina", "Liam",]
                            #   ,4)

def print_players(player_ids):
    # print(player_ids)
    for id in player_ids:
        player = tournament.players[id]
        print(id, player.score)
    print()
    result_list = []
    for player in player_ids:
        result_list.append(player[0])
    print(result_list)

    for player in player_ids:
        s = ""
        for closest in get_closest_players(player, player_ids):
            s += f"{closest[0]}, "
        s = s.strip(", ")
        print(f"{player[0]}, [{s}]")
        # l = []
        # played_with = tournament.players[player].played_with
        # for oppo in player_ids:
        #     if not oppo in played_with and not oppo == player:
        #         l.append(oppo[0])
        # print(f"{player[0], l}")

def closest_players_v0(player_ids: list, player):
    # this function assumes player_ids is already sorted by score
    closest_players = []
    played_with = tournament.players[player].played_with
    index = player_ids.index(player)
    h = index -1
    j = index +1
    over = False
    while not over:
        if j < len(player_ids):
            if player_ids[j] not in played_with:
                closest_players.append(player_ids[j])
            j += 1
        if h >= 0:
            if player_ids[h] not in played_with:
                closest_players.append(player_ids[h])
            h -= 1
        if j >= len(player_ids) and h < 0:
            over = True
    return closest_players

def print_turn(turn: model.Turn):
    print(turn.name)
    print(turn.start_time)
    print(turn.end_time)
    for match in turn.matchs:
        print(match)
    print()

def make_pairs(player_ids: list):
    # associer par paires les joueurs dans l'ordre j1 avec j2 ect
    # si j1 a déjà joué contre j2 associer avec j3
    pairs = []
    players = player_ids.copy()
    pairs_valid = True

    # Regarder si les paires sont valides
    for i in range (0, len(players), 2):
        p1 = players[i]
        p2 = players[i+1]
        if p2 in played_with(p1):
            print(colored(f"{p1} and {p2} already played", 'cyan'))
            pairs_valid = False
            break
        else:
            pairs.append((p1,p2))
            print(colored((p1,p2), 'green'))
    
    # Si une erreur dans les paires:
    if not pairs_valid:
        print(colored("Sorting best pairs", 'cyan'))
        pairs = sort_best_pairs(players)
    
    # mettre à jour la liste des joueurs joués avec
    for pair in pairs:
        p1 = pair[0]
        p2 = pair[1]
        tournament.players[p1].played_with.append(p2)
        tournament.players[p2].played_with.append(p1)

    return pairs

def sort_best_pairs(players: list):
    pairs = []
    best_dict = {}
    # Générer un dict de listes dont les clés sont les joueurs ordonnés par leur score croissant
    # chaque liste contient chaque chaque joueur n'ayant pas joué avec le joueur correspondant
    # la liste est ordonné du joueur le plus "proche" en terme de place dans la liste initiale au plus éloigné

    for player in players:
        # générer la liste des joueurs les plus proches
        best_dict[player] = get_closest_players(player, players)
    
    # Prendre la première paire à la fin du dic
    pair = get_pair_from_dict(best_dict, players[-1])
    if pair == False:
        pair = get_next_best_pair(players, players[-1], best_dict)
    pairs.append(pair)
    print_dict(best_dict)

    # Pairer le joueur ayant le moins d'adversaires possible tant que le dict n'est pas vide
    while best_dict:
        least_player = min(best_dict, key=lambda x: len(best_dict[x]))
        pair = get_pair_from_dict(best_dict, least_player)

        # Cas exceptionnel: si le joueur donné n'a plus aucun adversaire disponible
        if pair == False:
            pair = get_next_best_pair(players, least_player, best_dict)
                
        pairs.append(pair)
        print_dict(best_dict)
    
    return pairs

def get_next_best_pair(player_ids:list, least_player, best_dict: dict):
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
            j+=1
        if not hb or over:
            ph = player_ids[h]
            if ph in best_dict.keys():
                p2 = ph
                over = True
            h-=1
    pair = (p1, p2)
    print(colored(f"Exceptionnaly pairing {p1} and {p2}", 'red'))
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

def print_dict(d: dict):
    for key in d.keys():
        l = []
        players = d[key]
        for player in players:
            l.append(player[0])
        print(colored(f"{key[0]}: {l}", "yellow"))

def get_pair_from_dict(d: dict, player_id):
    # pairer la clé du dict (p1) avec le premier joueur de la liste de p1
    # Supprimer les clés de la paire ainsi que leur instances des les listes restantes
    p1 = player_id
    if len(d[p1]) == 0:
        print(colored(f"{p1} had no available opponent", 'red'))
        return False


    p2 = d.pop(p1)[0]
    print(colored(f"{p1}, {p2} \n", 'green'))
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

def get_closest_players(player, players):
    # générer la liste des joueurs les plus proches
    l = []
    index = players.index(player)
    over = False
    j = index +1
    h = index -1
    p_with = played_with(player)

    while not over:
        jb = j == len(players)
        hb = h == -1
        
        if not jb:
            pj = players[j]
            if not pj in p_with:
                l.append(pj)
            j+=1
        if not hb:
            ph = players[h]
            if not ph in p_with:
                l.append(ph)
            h-=1
        if jb and hb:
            over = True
    
    return l

def played_with(player_id):
    return tournament.players[player_id].played_with


def make_pairsv_0(player_ids: list, iterate_from_end = False):
    # associer par paires les joueurs dans l'ordre j1 avec j2 ect
    # si j1 a déjà joué contre j2 associer avec j3
    pairs = []
    
    # Associer chaque joueurs 2 par 2 dans l'ordre de l'array (score croissant)
    # Si l'un des joueurs a déjà joué contre un autre joueur, 
    # regarder chaque joueurs suivant jusqu'à trouver un contre qui n'a pas joué
    # initialiser la liste de paires avec la paire trouvé, et celles d'avant, recommencer la boucle
    
    # ??? relancer cette boucle jusqu'à ce qu'aucune erreur ne soit trouvé
    players = player_ids

    start = 0
    end = len(players)
    step = 2
    if iterate_from_end:
        start = end
        end = 0
        step = -2
    # Regarder chaque paire de joueurs dans l'ordre de l'array (score croissant)
    for i in range(start, end, step):
        p1 = players[i]
        p2 = players[i+1]
        # Si les 2 joueurs ont déjà joué l'un contre l'autre, 
        if p2 in tournament.players[p1].played_with:
            print(colored(f"{p1} Already played {p2} !", 'yellow'))
            valid = False
            h = i-1
            j = i+2
            p2 = None

            # reached_score = lambda j, h: True if j >= len(players) and h < 0 else False
            # regarder le joueur suivant p2, puis le joueur précédent p1 
            # jusqu'à trouver un qui n'a pas déjà joué contre
            while not valid:
                print(colored("Searching new pair", 'yellow'))
                time.sleep(0.05)
                if j < len(players):
                    pj = players[j]
                    if not pj in tournament.players[p1].played_with:
                        print(colored(f"Pairing {p1} with next player {pj}", 'cyan'))
                        p2 = players.pop(j)
                        valid = True
                        continue
                    else:
                        print(colored(f"nextplayer {pj} was played with", 'cyan'))
                        j += 1
                else:
                    print(colored(f"Reached end of player list: {j}", 'cyan'))
                if h >= 0:
                    ph = players[h]
                    if not ph in tournament.players[p1].played_with:
                        print(colored(f"Pairing {p1} with previous player {ph}", 'light_blue'))
                        p2 = players.pop(h)
                        valid = True
                        continue
                    else:
                        print(colored(f"previousplayer {ph} was played with", 'light_blue'))
                        h -= 1
                else:
                    print(colored(f"Reached start of player list: {h}", 'light_blue'))
            
            # pop et insert après le premier joueur le joueur trouvé dans l'array
            if not p2 == None:
                print(colored(players, 'magenta'))
                print(colored(f"Inserting {p2} at {i+1}", 'magenta'))
                players.insert(i+1, p2)
            else:
                print(colored("Error: p2 is None !", 'red'))
                print_players(player_ids)
                        
        pairs.append((p1, p2))

    paired_players = []
    for pair in pairs:
        print(colored(pair, 'green'))
        if pair[0] in tournament.players[pair[1]].played_with:
            print(colored(f"Error: {pair[0]} already played {pair[1]}", 'red'))
            return False
        if pair[1] in tournament.players[pair[0]].played_with:
            print(colored(f"Error: {pair[1]} already played {pair[0]}", 'red'))
            return False

        tournament.players[pair[0]].played_with.append(pair[1])
        tournament.players[pair[1]].played_with.append(pair[0])

        if pair[0] not in paired_players:
            paired_players.append(pair[0])
        else:
            print(colored(f"Error: {pair[0]} already paired !", 'red'))
            return False
        if pair[1] not in paired_players:
            paired_players.append(pair[1])
        else:
            print(colored(f"Error: {pair[1]} already paired !", 'red'))
            return False
    
    return pairs
    # avlb_players = player_ids
    
    # while len(avlb_players)> 0:
    # # pop le prochain joueur
    #     p1 = avlb_players.pop(0)
    #     for i in range(len(avlb_players)):
    #         # regarder le joueur d'après et vérifier si a déjà joué contre eux
    #         # si oui continuer de regarder le joueur d'après
    #         if avlb_players[i] not in tournament.players[p1].played_with:
    #             # une fois un nouveau joueur trouvé pop ce joueur est créer une paire
    #             p2 = avlb_players.pop(i)
    #             tournament.players[p1].played_with.append(p2)
    #             tournament.players[p2].played_with.append(p1)
    #             break
    #     # continuer la boucle
    #     pairs.append((p1, p2))

def generate_rand_matchs(pairs):
    matchs = []
    for pair in pairs:
        p0_score = 0
        p1_score = 0
        r = random.randint(0,2)
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

def update_players_score(matchs):
    for match in matchs:
        tournament.players[match[0][0]].score += match[0][1]
        tournament.players[match[1][0]].score += match[1][1]

if __name__ == "__main__":

    for i in range(tournament.turn_number):
        turn = model.Turn(f"Round {i+1}", 0)
        print("Start of Round ", i+1)

        # Prendre liste de joueurs trié
        player_ids = tournament.sorted_player_ids()
        print_players(player_ids)
        
        # Faire des paires de joueurs
        player_pairs = make_pairs(player_ids)
        print()
        
        # Prendre des résultats de matchs
        matchs = generate_rand_matchs(player_pairs)
        # for match in matchs:
        #     print(match)
        # print()

        # Ajuster score des joueurs
        update_players_score(matchs)

        # Enregistrer matchs
        turn.matchs = matchs
        turn.end_time = 10

        tournament.turns.append(turn)

        # Prochain tour
    
    print("End results: ")
    player_ids = tournament.sorted_player_ids()
    print_players(player_ids)
    

    # print(f"{player} played with: {tournament.players[player].played_with}")

