from view import view
# from model import model


class Controller:
    # def __init__(self):
    #     self.start()

    def start(self):
        view.starting_screen()

        while True:
            input = self.get_user_input()
            if input == "Quitter":
                print("\n\n Fermeture de Chess Tournament Helper. \n\n")
                break
            else:
                print(f"{input} n'est pas une commande reconnu.")

    def get_user_input(self):
        return input()
