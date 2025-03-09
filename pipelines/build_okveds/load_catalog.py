import pickle

# Загружаем данные из бинарного файла
with open("okved_data.pkl", "rb") as file:
    loaded_data = pickle.load(file)

print(loaded_data)