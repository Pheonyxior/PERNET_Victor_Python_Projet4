import os

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
data_path = os.path.dirname(dir_path)
print(data_path)
data_path += f"{os.sep}data{os.sep}player_database.json"
print(data_path)
