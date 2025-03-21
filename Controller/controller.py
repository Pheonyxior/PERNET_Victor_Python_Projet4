from view import view
from model import model
import json
import os
from enum import Enum
from enum import auto

QUIT_CMD = "Q"
init_player_info = {}
init_tournament_info = {}


class start_cmd(Enum):
    CREATE_TOURNAMENT = auto()
    ADD_tournament = auto()
    TOURNAMENT_LIST = auto()
    tournament_LIST = auto()


class Controller:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        # print(dir_path)

    def start(self):
        view.starting_screen()

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
                    case start_cmd.ADD_tournament.value:
                        self.add_player()
                        view.start_menu()
                    case start_cmd.TOURNAMENT_LIST.value:
                        print("TOURNAMENT_LIST")
                    case start_cmd.tournament_LIST.value:
                        print("tournament_LIST")
                    case _:
                        print(f"{user_input} n'est pas une commande reconnu.")

    def create_tournament(self):
        view.create_tournament()
        name = input("Nom du tournoi: ")
        place = input("Lieu du tournoi: ")
        start_date = input(
            "Date de début du tournoi (dd/mm/YYYY): ")
        end_date = input(
            "Date de fin du tournoi (dd/mm/YYYY): ")

        new_tournament = model.Tournament(name, place, start_date, end_date)
        self.register_tournament_to_database(new_tournament)

    def add_player(self):
        view.add_player()
        surname = input("Nom de famille du joueur: ")
        name = input("Prénom du joueur: ")
        date = input(
            "Date de naissance du joueur (dd/mm/YYYY): ")
        id = input(
            "Identifiant national d’échecs du joueur: ")
        # Check if id is valid
        new_player = model.Player(surname, name, date, id)
        self.register_player_to_database(new_player)

    def register_tournament_to_database(self, tournament: model.Tournament):
        tournament_info = {
            tournament.name: {
                "Lieu": tournament.place,
                # Scinder dates
                "Date de début et de fin": f"{
                    tournament.start_date} | {tournament.end_date}",
                "Nombre de tours": tournament.turn_number,
                "Tours": tournament.turns,
                "Joueurs": tournament.registered_players,
                "Description": tournament.description
            }
        }
        json_object = json.dumps(tournament_info, indent=4)
        file_path = self.dir_path + f"{
            os.sep}data{os.sep}tournaments{os.sep}tournament_data.json"
        print(file_path)
        with open(file_path, "a") as file:
            try:
                file.write(json_object)
                print(
                    tournament.name, " a été sauvegardé dans le fichier "
                    "tournament_database.json."
                    )
            except Exception as e:
                print(""
                      "Sauvegarde dans le fichier "
                      "tournament_database.json échoué: ", e
                      )

    def register_player_to_database(self, player: model.Player):
        player_info = {
            player.chess_id: {
                "Nom": player.surname,
                "Prénom": player.name,
                "Date de naissance": player.date_of_birth,
            }
        }
        json_object = json.dumps(player_info, indent=4)
        file_path = self.dir_path + f"{
            os.sep}data{os.sep}player_database.json"
        print(file_path)
        with open(file_path, "a") as file:
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
