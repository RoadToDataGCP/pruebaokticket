import random

def obtenernameid(empresas):
    nombreid = list()
    for _, empresa in empresas.iterrows():
        nombreid1 = {
            'name': empresa["name"],
            'id': empresa["id"]
        }
        nombreid.append(nombreid1)
    return nombreid


    

