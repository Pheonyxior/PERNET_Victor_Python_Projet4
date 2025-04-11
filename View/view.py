import prettytable as pretty


def starting_screen():
    print("\n\n     Chess Tournament Helper \n\n")
    start_menu()


def start_menu():
    print("Rentrer le nombre indiqué pour executer la commande "
          "correspondante.\n"
          "Rentrer 'Q' pour fermer le programme.\n")
    print("1: Créer un nouveau tournoi.\n"
          "2: Ajouter un joueur.\n"
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
        "Num.", "Nom", "Lieu", "Date de début", "Date de fin", "Nombre de tours", "Tours",
        "Joueurs enregistrés", "Description"]

    for tournament_key in data.keys():
        tournament = data[tournament_key]
        row = [tournament_key]
        for key in tournament:
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
