import json

def rectificar_historial():
    with open('../ChatBot/config/history.json', 'r') as file:
        config = json.load(file)
    if config['history'] == True:
        rute = ["../ChatBot/data","../ChatBot/data/files"]
    elif config['history'] == False:
        rute = ["../ChatBot/old_data","../ChatBot/old_data/old_files"]
    print(rute)
    rutas = rute
    return rutas

