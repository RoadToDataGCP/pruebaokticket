import constantes
import requests as rq
from controlerrores import control_errores
import json
import pandas as pd
import os

CABECERAUSUARIOS = [
            'id', 
            'name', 
            'email', 
            'id_role', 
            'status_id', 
            'company_type_id',
            'currency', 
            'app_version', 
            'legal_texts_version',
            'pop_checked',
            'tyc_checked',
            'created_at',
            'updated_at',
            'deleted_at',
            'active_company',
            'active_department',
            'custom_id',
            'custom_id_2',
            'custom_id_3',
            'language',
            'active',
            'last_login_date',
            'login_error_count',
            'skip_sso',
            'companies']

def create_user(nombreempresa, name, email, password, ids_companies, custom_id, custom_id2, custom_id3):
    url = f'{os.getenv('HOST')}/api/users'
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'company': nombreempresa
    }
    payload = {
        'name' : name,
        'email': email,
        'password': password,
        'currency': 21,
        'legal_texts_version': 1,
        'ids_companies[<company>][id_role]': 3,
        'id_role': 3,
        'ids_companies': ids_companies,
        'custom_id': custom_id,
        'custom_id_2': custom_id2,
        'custom_id_3': custom_id3,
        'costs_centers[]': 21
    }

    respuesta = rq.post(url, headers=headers, json=payload)
    datos = control_errores(respuesta)
    # Imprimir datos con formato legible
    print(json.dumps(datos, indent=4, ensure_ascii=False))

def obtener_lista_total_usuarios():
    url = f'{os.getenv('HOST')}/api/users?with=companies'
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    respuesta = rq.get(url, headers=headers)
    datos = control_errores(respuesta)
    # Imprimir datos con formato legible
    return datos
def crear_csv_usuarios(datos):
    datos = datos['data']
    listausuarios = list()
    for user in datos:
        #companies = user.get("companies", [])
        #company_id = companies[0]["id"] if companies else None  # Evita el error
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
    csvususarios.to_csv("usuarios.csv", mode="w", header=CABECERAUSUARIOS, index=False)
    return csvususarios


#NO SE UTILIZA
def obtener_mi_usuario():
    url = f'{os.getenv('HOST')}/api/me?with=companies'
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Accept': 'application/json'
    }

    respuesta = rq.get(url, headers=headers)
    datos = control_errores(respuesta)
    print(json.dumps(datos))


def borrar_usuario(nombreempresa, name, email, password):
    url = f'{os.getenv('HOST')}/api/me?with=companies'
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'company' : nombreempresa
    }
    payload = {
        'name' : name,
        'email': email,
        'password': password,
    }
    respuesta = rq.delete(url, headers=headers, json=payload)
    datos = control_errores(respuesta)
    print(json.dumps(datos))


