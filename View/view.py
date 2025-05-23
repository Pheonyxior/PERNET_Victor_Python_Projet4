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


def tournament_list(data: dict):
    print("Afficher la liste des tournois enregistrés sur la base de donnée.\n")

    table = pretty.PrettyTable()
    table.field_names = [
        "Num.", "Nom", "Lieu", "Date de début", "Date de fin", "Nombre de tours",
        "Joueurs enregistrés", "Description"]

    for tournament_key in data.keys():
        tournament = data[tournament_key]
        row = [tournament_key]
        for key in tournament:
            if key == "turns": continue
            row.append(tournament[key])
        table.add_row(row)

    print(table, "\n")


def player_list(data: dict):
    print("Afficher la liste des joueurs enregistrés sur la base de donnée.\n")

    i = 0
    table = pretty.PrettyTable()
    table.field_names = [
        "Num.", "Nom", "Prénom", "Date de naissance", "Identifiant national d’échecs"]

    for player_key in data.keys():
        player = data[player_key]
        row = [i]
        for key in player.keys():
            row.append(player[key])
        row.append(player_key)
        table.add_row(row)
        i += 1

    print(table, "\n")


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
    for player in tournament.sorted_player_ids(reverse = True):
        table.add_row([player_dic[player]["surname"], tournament.players[player].score])
    
    print('\n', table, '\n')
    # table = pretty.PrettyTable()
    # table.field_names = ["J1", "J1 G/P", "J1 Score",
    #                      "J2", "J2 G/P", "J2 Score"]
    # for match in matchs:
    #     p1 = tournament.players[match[0][0]]
    #     w1 = "MN"
    #     if match[0][1] == 1:
    #         w1 = 'G'
    #     elif match[0][1] == -1:
    #         w1 = 'P'
    #     r1 = [player_dic[p1.id]["surname"], w1, p1.score]
    #     p2 = tournament.players[match[1][0]]
    #     w2 = "MN"
    #     if match[1][1] == 1:
    #         w2 = 'G'
    #     elif match[1][1] == -1:
    #         w2 = 'P'
    #     r2 = [player_dic[p2.id]["surname"], w2, p2.score]
    #     table.add_row(r1 + r2)
        
    # print(table)
    