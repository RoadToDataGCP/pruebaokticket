import random
import pandas as pd
import constantes


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


def crearCsvUsuarios(datos):
    datos = datos['data']
    listausuarios = list()
    for user in datos:
        fila = {
            'id' : user['id'] , 
            'name': user['name'], 
            'email': user['email'], 
            'id_role': user['id_role'] , 
            'status_id': user['status_id'], 
            'company_type_id': user['company_type_id'],
            'currency': user['currency'], 
            'app_version': user['app_version'], 
            'legal_texts_version': user[ 'legal_texts_version'],
            'pop_checked': user['pop_checked'],
            'tyc_checked': user['tyc_checked'],
            'created_at': user['created_at'],
            'updated_at': user['updated_at'],
            'deleted_at': user['deleted_at'],
            'active_company': user['active_company'],
            'active_department': user['active_department'],
            'custom_id': user['custom_id'],
            'custom_id_2': user['custom_id_2'],
            'custom_id_3': user['custom_id_3'],
            'language': user['language'],
            'active': user['active'],
            'last_login_date': user['last_login_date'],
            'login_error_count': user['login_error_count'],
            'skip_sso': user['skip_sso'],
            'companies' : user["companies"][0]["id"] 
        }
        listausuarios.append(fila)
    csvususarios = pd.DataFrame(listausuarios)
    csvususarios.to_csv("usuarios.csv", mode="w", header=constantes.CABECERAUSUARIOS, index=False)
    return csvususarios
