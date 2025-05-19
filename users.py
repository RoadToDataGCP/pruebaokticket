import constantes
import requests as rq
from controlerrores import controlErrores
import json
import pandas as pd


def obtenerListaTotalEmpresas():
  url = "https://apipre.okticket.es/v2/public/api/companies"

  payload={}
  headers = {
    'Authorization': f'Bearer {constantes.TOKEND}',
    'Accept': 'application/json'
  }
  
  respuesta = rq.get(url, headers=headers)
  datos = controlErrores(respuesta)
  
  return datos

def createUser(nombreempresa, name, email, password, ids_companies, custom_id, custom_id2, custom_id3):
    url = f'{constantes.HOST}/api/users'
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
    datos = controlErrores(respuesta)
    print(datos)

def obtenerListaTotalUsuarios():
    url = f'{constantes.HOST}/api/users?with=companies'
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    respuesta = rq.get(url, headers=headers)
    datos = controlErrores(respuesta)
    return datos
    
def obtenerMiUsuario():
    url = f'{constantes.HOST}/api/me?with=companies'
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Accept': 'application/json'
    }

    respuesta = rq.get(url, headers=headers)
    datos = controlErrores(respuesta)
    print(json.dumps(datos))

def borrarUsuario(iduser):
    url = f'{constantes.HOST}/api/users/{iduser}'
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        
    }
    payload = {
        
    }
    respuesta = rq.delete(url, headers=headers, json=payload)
    datos = controlErrores(respuesta)
    print(json.dumps(datos))
