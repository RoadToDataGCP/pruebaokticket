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


def obtenernameid2(empresas):
    nombreid = list()
    listaemp = empresas['data']
    for emp in listaemp:
        nombreid1 = {
            'name': emp["name"],
            'id': emp["id"]
        }
        nombreid.append(nombreid1)
    return nombreid

def obteneruseridempresaid(usuarios):
    useridempid = list()
    listausuarios= usuarios['data']
    for user in listausuarios:
        useidempid1 = dict()
        useidempid1['iduser'] = user['id']
        listaemp =  user['companies']
        for emp in listaemp:
            useidempid1['idemp'] = emp['id']
        useridempid.append(useidempid1)
    return useridempid
