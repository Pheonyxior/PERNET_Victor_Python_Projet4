import prettytable as pretty


def starting_screen():
    print("\n\n     Chess Tournament Helper \n\n")
    start_menu()


def start_menu():
    print("\nRentrer le nombre indiqué pour executer la commande "
          "correspondante.\n"
          "Rentrer 'Q' pour fermer le programme.\n")
    print("1: Ajouter un nouveau tournoi à la base de donnée.\n"
          "2: Ajouter un joueur à la base de donnée.\n"
          "3: Liste des tournois.\n"
          "4: Liste des joueurs et joueuses.\n")


def create_tournament():
    print("Créer un nouveau tournoi.\n"
          "Veuillez entrer les informations suivantes: \n")


def add_player():
    print("Ajouter un joueur à la base de donnée des joueurs.\n"
          "Veuillez entrer les informations suivantes: \n")


def tournament_list(data: dict, player_dict: dict):
    print("Afficher la liste des tournois enregistrés sur la base de donnée.\n")

    table = pretty.PrettyTable(max_width=40)
    table.field_names = [
        "Num.", "Nom", "Lieu", "Date de début", "Date de fin", "Nombre de tours",
        "Joueurs enregistrés", "Description"]

    for tournament_key in data.keys():
        tournament = data[tournament_key]
        row = [tournament_key]
        for key in tournament:
            if key == "turns":
                continue
            if key == "registered_players":
                sorted_players = []
                for chess_id in tournament[key]:
                    player = player_dict[chess_id]
                    sorted_players.append(player["name"])
                sorted_players.sort(key=str.casefold)
                row.append(sorted_players)
                continue
            row.append(tournament[key])
        table.add_row(row)

    print(table, "\n")


def player_list(data: dict):
    print("Afficher la liste des joueurs enregistrés sur la base de donnée.\n")

    i = 0
    table = pretty.PrettyTable()
    table.field_names = [
        "Num.", "Nom", "Prénom", "Date de naissance", "Identifiant national d’échecs"]

    new_list = list(data.values())
    new_list.sort(key=lambda d: d['name'])

    for player_key in data.keys():
        player = data[player_key]
        row = [i]
        print(new_list[i])
        for key in new_list[i]:
            row.append(new_list[i][key])
        row.append(player_key)
        table.add_row(row)
        i += 1

    print(table, "\n")
    for player in new_list:
        print(player)


def print_tournament_turns(turns, tournament_name, player_dic):
    print(f"Afficher les rounds du {tournament_name}.\n")

    for turn in turns:
        print(f"{turn["name"]}, commencé à {turn["start_time"]}, fini à {turn["end_time"]}:")
        table = pretty.PrettyTable(max_width=40)
        table.field_names = ["Match", "Résultats"]
        for match in turn["matchs"]:
            match_data = []
            p0 = player_dic[match[0][0]]["surname"]
            p1 = player_dic[match[1][0]]["surname"]
            match_data.append(f"{p0} / {p1}")
            if match[0][1] == 1:
                match_data.append("Gagné / Perdu")
            elif match[1][1] == 1:
                match_data.append("Perdu / Gagné")
            else:
                match_data.append("Match Nulle")

            table.add_row(match_data)
        print(table, '\n')


def print_turn_start(turn_name, player_dic, pairs, tournament):
    print(f"\n Début du {turn_name}. \n")

    table = pretty.PrettyTable()
    table.field_names = ["J1", "J1 Score",
                         "J2", "J2 Score"]
    for pair in pairs:
        p0 = tournament.players[pair[0]]
        r0 = [player_dic[p0.id]["surname"], p0.score]
        p1 = tournament.players[pair[1]]
        r1 = [player_dic[p1.id]["surname"], p1.score]
        table.add_row(r0 + r1)

    print(table, '\n')


def print_turn_result(player_dic, tournament):
    table = pretty.PrettyTable()
    table.field_names = ["Joueur", "Score"]
    for player in tournament.sorted_player_ids(reverse=True):
        table.add_row([player_dic[player]["surname"], tournament.players[player].score])

    print(table, '\n')
