from view import view
from model import model
import json
import os
from enum import Enum
from enum import auto
from datetime import datetime

# prototyping packages
from random_strings import random_string
import random
import names as name_gen
from random_words import RandomWords as word_gen

QUIT_CMD = "Q"
player_dic = {}
tournament_dic = {}


class start_cmd(Enum):
    CREATE_TOURNAMENT = auto()
    ADD_TOURNAMENT = auto()
    TOURNAMENT_LIST = auto()
    PLAYER_LIST = auto()


class cheat_cmd(Enum):
    RAND = "rand"


class Controller:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        # print(dir_path)

    def start(self):
        self.get_tournament_database()
        self.get_player_database()

        view.starting_screen()
        self.handle_user_input()

    def handle_user_input(self):
        while True:
            user_input = input()
            try:
                user_input = int(user_input)
            except Exception:
                pass
            match user_input:
                case 1:
                    self.create_tournament()
                case 2:
                    self.add_player()
                case 3:
                    view.tournament_list(tournament_dic)
                    self.tournament_list(tournament_dic)
                case 4:
                    view.player_list(player_dic)
                case "Q":
                    # remplacer par q gérer majuscule minuscule
                    print("\n\n Fermeture de Chess Tournament Helper. \n\n")
                    break
                case _:
                    print(f"{user_input} n'est pas une commande reconnu.")
            view.start_menu()

    def create_tournament(self):
        view.create_tournament()
        name = input("Nom du tournoi: ")
        if name == cheat_cmd.RAND.value:
            rw = word_gen()
            n = rw.random_word()
            name = n + " tournament"
            n = rw.random_word()
            place = n
            start_date = str(f"{random.randint(0, 31)}/{random.randint(0, 12)}/{random.randint(2000, 2100)}")
            end_date = str(f"{random.randint(0, 31)}/{random.randint(0, 12)}/{random.randint(2000, 2100)}")
        else:
            place = input("Lieu du tournoi: ")
            start_date = input("Date de début du tournoi (dd/mm/YYYY): ")
            end_date = input("Date de fin du tournoi (dd/mm/YYYY): ")

        new_tournament = model.Tournament(name, place, start_date, end_date)
        self.register_tournament_to_database(new_tournament)
        self.get_tournament_database()

    def get_tournament_database(self):
        global tournament_dic

        file_path = self.dir_path + f"{os.sep}data{os.sep}tournaments{os.sep}tournament_data.json"
        with open(file_path, "r") as file:
            try:
                tournament_dic = json.load(file)
                # tournament_dic = dic
                # for key in dic.keys():
                #     t = dic[key]
                #     tournament_data = model.Tournament(
                #         key, t["place"], t["start_date"], t["end_date"], t["turn_number"], t["description"])
                #     tournament_dic[key] = tournament_data
                print("Base de donnée tournament_data.json chargée.")
            except Exception as e:
                print("Echec du chargement de la base de donnée tournament_data.json : ", e)

    def register_tournament_to_database(self, tournament: model.Tournament, db_key=-1):
        global tournament_dic
        turns = []
        for turn in tournament.turns:
            turns.append({
                    "name": turn.name,
                    "start_time": turn.start_time,
                    "end_time": turn.end_time,
                    "matchs": turn.matchs
                }
            )

        key = db_key
        if key == -1:
            key = len(tournament_dic)

        tournament_dic[key] = {
                "name": tournament.name,
                "place": tournament.place,
                # Scinder dates
                "start_date": tournament.start_date,
                "end_date": tournament.end_date,
                "turn_number": tournament.turn_number,
                "turns": turns,
                "registered_players": tournament.registered_players,
                "description": tournament.description
            }
        self.write_tournaments_to_database(tournament.name)

    def write_tournaments_to_database(self, tournament_name=""):
        json_object = json.dumps(tournament_dic, indent=4)
        file_path = self.dir_path + f"{
            os.sep}data{os.sep}tournaments{os.sep}tournament_data.json"
        # print(file_path)
        with open(file_path, "w") as file:
            try:
                file.write(json_object)
                print(tournament_name, " a été sauvegardé dans le fichier tournament_database.json.")
            except Exception as e:
                print("Sauvegarde dans le fichier tournament_database.json échoué: ", e)

    def add_player(self):
        view.add_player()
        surname = input("Nom de famille du joueur: ")
        if surname == cheat_cmd.RAND.value:
            # n: str = name_gen.get_full_name()
            # n = n.split(" ", 1)
            surname = name_gen.get_first_name()
            name = name_gen.get_last_name()
            date = str(f"{random.randint(0, 31)}/{random.randint(1, 12)}/{random.randint(1950, 2050)}")
            id = str(f"{random_string(2)}"
                     f"{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
                     f"{random.randint(0, 9)}{random.randint(0, 9)}")
            while id in player_dic.keys():
                id = str(f"{random_string(2)}"
                         f"{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
                         f"{random.randint(0, 9)}{random.randint(0, 9)}")
        else:
            name = input("Prénom du joueur: ")
            date = input(
                "Date de naissance du joueur (dd/mm/YYYY): ")
            id = input(
                "Identifiant national d’échecs du joueur: ")
        # TODO Check if id is valid (respecte le formattage et n'est pas déjà enregistré)
        new_player = model.Player(surname, name, date, id)
        self.register_player_to_database(new_player)
        self.get_player_database()

    def get_player_database(self):
        global player_dic

        file_path = self.dir_path + f"{os.sep}data{os.sep}player_database.json"
        with open(file_path, "r") as file:
            try:
                player_dic = json.load(file)
                print("Base de donnée player_database.json chargée.")
            except Exception as e:
                print("Echec du chargement de la base de donnée player_database.json : ", e)

    def register_player_to_database(self, player: model.Player):
        global player_dic

        player_dic[player.chess_id] = {
                "surname": player.surname,
                "name": player.name,
                "date_of_birth": player.date_of_birth,
            }

        json_object = json.dumps(player_dic, indent=4)
        file_path = self.dir_path + f"{
            os.sep}data{os.sep}player_database.json"
        # print(file_path)
        with open(file_path, "w") as file:
            try:
                file.write(json_object)
                print(
                    player.name, " a été sauvegardé dans le fichier "
                    "player_database.json."
                    )
            except Exception as e:
                print(""
                      "Sauvegarde dans le fichier "
                      "player_database.json échoué: ", e
                      )

    def tournament_list(self, tournament_data: dict):
        cmd = ("Rentrer le nombre indiqué pour executer la commande correspondante \n"
               "1: Commencer un tournoi.\n"
               "2: Ajouter des joueurs à un tournoi.\n"
               "3: Modifier la description d'un tournoi.\n"
               "4: Afficher les rounds d'un tournoi.\n"
               "5: Retour.")
        print(cmd)
        valid = False
        while not valid:
            valid = True
            user_input = input()
            try:
                user_input = int(user_input)
            except Exception:
                pass
            match user_input:
                case 1:
                    self.start_tournament(tournament_data)
                case 2:
                    self.add_player_to_tournament(tournament_data)
                case 3:
                    cmd = "Rentrer le numéro du tournoi dont modifier la description: "
                    user_input = input(cmd)
                    while not user_input.isnumeric() or user_input not in tournament_data.keys():
                        user_input = input(f"{user_input} n'est pas valable.\n{cmd}")
                    t_key = str(user_input)

                    user_input = input("Rentrer une nouvelle description: ")
                    tournament_data[t_key]["description"] = user_input
                    self.write_tournaments_to_database(tournament_data[t_key]["name"])
                case 4:
                    cmd = "Rentrer le numéro du tournoi dont afficher les rounds: "
                    user_input = input(cmd)
                    while not user_input.isnumeric() or user_input not in tournament_data.keys():
                        user_input = input(f"{user_input} n'est pas valable.\n{cmd}")
                    t_key = str(user_input)

                    tournament = tournament_data[t_key]
                    view.print_tournament_turns(tournament["turns"], tournament["name"], player_dic)

                case 5: return

                case _:
                    print(f"{user_input} n'est pas une commande reconnu.")
                    valid = False

    def start_tournament(self, tournament_data):
        cmd = "Rentrer le numéro du tournoi à commencer: "
        user_input = input(cmd)
        while not user_input.isnumeric() or user_input not in tournament_data.keys():
            user_input = input(f"{user_input} n'est pas valable.\n{cmd}")
        t_key = str(user_input)

        tourn_dict = tournament_data[t_key]
        tournament = self.get_tournament(tourn_dict)
        # Si on reprend un tournoi en cours, on print les derniers résultats
        if not tournament.current_turn == 0:
            if tournament.current_turn == tournament.turn_number:
                print(f"{tournament.name} a atteint le nombre de tour maximal et est donc considéré terminé.\n")
                return
            print("Reprise du tournoi à partir du Round", tournament.current_turn + 1)
            view.print_turn_result(player_dic, tournament)

        for i in range(tournament.current_turn, tournament.turn_number):
            # TODO prendre date et heure actuelle
            turn = model.Turn(f"Round {i+1}", datetime.now().ctime())
            tournament._current_turn = i

            player_ids = tournament.sorted_player_ids()
            player_pairs = tournament.make_pairs(player_ids)

            cmd = f"Commencer le {turn.name} ? (o/n) "
            valid = False
            while not valid:
                valid = True
                user_input = input(cmd)
                if user_input == 'o':
                    pass
                elif user_input == 'n':
                    print(f"{tournament.name} mit en pause au {turn.name}.\n")
                    return
                else:
                    valid = False
                    print(f"{user_input} n'est pas reconnu.")

            view.print_turn_start(turn.name, player_dic, player_pairs, tournament)
            matchs = []

            for pair in player_pairs:
                cmd = f"Est-ce que {player_dic[pair[0]]["surname"]} a gagné, perdu, ou match nulle ? (g/p/mn) "
                valid = False
                rand = False
                p0 = pair[0]
                p1 = pair[1]
                while not valid:
                    valid = True
                    user_input = input(cmd)
                    if user_input == 'g':
                        matchs.append(([p0, 1], [p1, -1]))
                    elif user_input == 'p':
                        matchs.append(([p0, -1], [p1, 1]))
                    elif user_input == "mn":
                        matchs.append(([p0, 0.5], [p1, 0.5]))
                    elif user_input == "rand":
                        rand = True
                    else:
                        valid = False
                        print(f"{user_input} n'est pas reconnu.")
                if rand:
                    matchs = tournament.generate_rand_matchs(player_pairs)
                    break

            tournament.update_players_score(matchs)
            view.print_turn_result(player_dic, tournament)
            turn.matchs = matchs
            # TODO prendre le temps actuel
            turn.end_time = datetime.now().ctime()
            tournament.turns.append(turn)

            self.register_tournament_to_database(tournament, t_key)

    def get_tournament(self, tourn_dict: dict):
        tournament = model.Tournament(
            tourn_dict["name"],
            tourn_dict["place"],
            tourn_dict["start_date"],
            tourn_dict["end_date"],
            tourn_dict["registered_players"],
            tourn_dict["turns"],
            tourn_dict["turn_number"],
            tourn_dict["description"]
        )
        return tournament

    def add_player_to_tournament(self, tournament_data):
        user_input = input("Rentrer le numéro du tournoi auquel ajouter un joueur: ")

        while not user_input.isnumeric() or user_input not in tournament_data.keys():
            user_input = input(f"{user_input} n'est pas valable.\n"
                               "Rentrer le numéro du tournoi auquel ajouter un joueur: ")
        t_key = str(user_input)

        add_more = True
        view.player_list(player_dic)
        while add_more:
            cmd = "Rentrer l'identifiant national d'échec du joueur (Q pour annuler): "
            user_input = input(cmd)
            valid_id = False
            while not valid_id:
                if user_input == 'Q':
                    return
                if user_input == "fill":
                    i = 0
                    for key in player_dic.keys():
                        tournament_data[t_key]["registered_players"].append(key)
                        i += 1
                        if i == 8:
                            self.write_tournaments_to_database(tournament_data[t_key]["name"])
                            return
                if user_input not in player_dic.keys():
                    user_input = input(f"{user_input} n'est pas présent dans la base de donnée.\n{cmd}")
                elif user_input in tournament_data[t_key]["registered_players"]:
                    user_input = input(f"{user_input} est déjà inscrit(e) à ce tournoi.\n{cmd}")
                else:
                    valid_id = True
            tournament_data[t_key]["registered_players"].append(user_input)
            self.write_tournaments_to_database(tournament_data[t_key]["name"])

            cmd = "Ajouter un autre joueur ? (o/n): "
            y_n = False
            while not y_n:
                y_n = True
                user_input = input(cmd)
                if user_input == 'o':
                    continue
                elif user_input == 'n':
                    add_more = False
                else:
                    print(f"{user_input} n'est pas reconnu.")
                    y_n = False


if __name__ == "__main__":
    ctrl = Controller()
    ctrl.start()
