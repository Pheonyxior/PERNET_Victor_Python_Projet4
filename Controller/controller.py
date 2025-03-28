from view import view
from model import model
import json
import os
from enum import Enum
from enum import auto

# prototyping packages
from random_strings import random_string
import random

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
        view.starting_screen()
        self.get_tournament_database()
        self.get_player_database()
        self.handle_user_input()

    def handle_user_input(self):
        while True:
            user_input = input()
            # remplacer par q gérer majuscule minuscule
            if user_input == QUIT_CMD:
                print("\n\n Fermeture de Chess Tournament Helper. \n\n")
                break
            else:
                user_input = int(user_input)
                match user_input:
                    case start_cmd.CREATE_TOURNAMENT.value:
                        self.create_tournament()
                        view.start_menu()
                    case start_cmd.ADD_TOURNAMENT.value:
                        self.add_player()
                        view.start_menu()
                    case start_cmd.TOURNAMENT_LIST.value:
                        print("TOURNAMENT_LIST")
                    case start_cmd.PLAYER_LIST.value:
                        print("PLAYER_LIST")
                    case _:
                        print(f"{user_input} n'est pas une commande reconnu.")

    def create_tournament(self):
        view.create_tournament()
        name = input("Nom du tournoi: ")
        print(cheat_cmd.RAND.value)
        print(name)
        if name == cheat_cmd.RAND.value:
            name = random_string(5) + " tournament"
            place = random_string(8)
            start_date = str(f"{random.randint(0, 31)}/{random.randint(0, 12)}/{random.randint(2000, 2100)}"),
            end_date = str(f"{random.randint(0, 31)}/{random.randint(0, 12)}/{random.randint(2000, 2100)}"),
        else:
            place = input("Lieu du tournoi: ")
            start_date = input("Date de début du tournoi (dd/mm/YYYY): ")
            end_date = input("Date de fin du tournoi (dd/mm/YYYY): ")

        new_tournament = model.Tournament(name, place, start_date, end_date)
        self.register_tournament_to_database(new_tournament)

    def get_tournament_database(self):
        global tournament_dic

        file_path = self.dir_path + f"{os.sep}data{os.sep}tournaments{os.sep}tournament_data.json"
        with open(file_path, "r") as file:
            try:
                tournament_dic = json.load(file)
                print("Base de donnée tournament_data.json chargée.")
            except Exception as e:
                print("Echec du chargement de la base de donnée tournament_data.json : ", e)

    def register_tournament_to_database(self, tournament: model.Tournament):
        global tournament_dic

        tournament_dic[tournament.name] = {
                "place": tournament.place,
                # Scinder dates
                "start_date": tournament.start_date,
                "end_date": tournament.end_date,
                "turn_number": tournament.turn_number,
                "turns": tournament.turns,
                "registered_players": tournament.registered_players,
                "description": tournament.description
            }

        json_object = json.dumps(tournament_dic, indent=4)
        file_path = self.dir_path + f"{
            os.sep}data{os.sep}tournaments{os.sep}tournament_data.json"
        # print(file_path)
        with open(file_path, "w") as file:
            try:
                file.write(json_object)
                print(tournament.name, " a été sauvegardé dans le fichier tournament_database.json.")
            except Exception as e:
                print("Sauvegarde dans le fichier tournament_database.json échoué: ", e)

    def add_player(self):
        view.add_player()
        surname = input("Nom de famille du joueur: ")
        if surname == cheat_cmd.RAND.value:
            surname = "Smith"+random_string(5)
            name = "John"+random_string(5)
            date = str(f"{random.randint(0, 31)}/{random.randint(0, 12)}/{random.randint(1950, 2050)}"),
            id = str(f"{random_string(2)}"
                     f"{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
                     f"{random.randint(0, 9)}{random.randint(0, 9)}")
        else:
            name = input("Prénom du joueur: ")
            date = input(
                "Date de naissance du joueur (dd/mm/YYYY): ")
            id = input(
                "Identifiant national d’échecs du joueur: ")
        # Check if id is valid
        new_player = model.Player(surname, name, date, id)
        self.register_player_to_database(new_player)

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


if __name__ == "__main__":
    ctrl = Controller()
    ctrl.start()
