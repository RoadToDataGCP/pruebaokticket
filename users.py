import constantes
import requests as rq
from controlerrores import controlErrores
import json
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("HOST")
def createUser(nombreempresa, name, email, password, ids_companies, custom_id, custom_id2, custom_id3):
    url = f'{host}/api/users'
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
    # Imprimir datos con formato legible
    print(json.dumps(datos, indent=4, ensure_ascii=False))

def obtenerListaTotalUsuarios():
    
    url = f'{host}/api/users?with=companies'
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    respuesta = rq.get(url, headers=headers)
    datos = controlErrores(respuesta)
    # Imprimir datos con formato legible
    return datos


def listado_email_users_de_empresa(idcompay):
  url = f'{host}/api/companies/{idcompay}/users'
  headers = {
      'Authorization': f'Bearer {constantes.TOKEND}',
      'Accept': 'application/json',
      'Content-Type': 'application/json',
  }

  respuesta = rq.get(url, headers=headers)
  datos = controlErrores(respuesta)

  listausers = list()
  usuarios= datos['data']
  for user in usuarios:
    idemailuser={
       'email': user['email'],
       'id' : user['id']
    }
    listausers.append(idemailuser)
  # Imprimir datos con formato legible
  return listausers

def asociar_usuario_a_dept(iduser,emailuser, idcompany, iddept):
    url = f'{host}/api/users/{iduser}'
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
    }
    payload = {
        "email": emailuser,
        "ids_companies": {
            idcompany: {
                "id_role": 2
            }	
        },
        "ids_departments": {
            iddept: {
                "id_role": 3
            }
        }
    }

    respuesta = rq.patch(url, headers=headers, json=payload)
    datos = controlErrores(respuesta)
    # Imprimir datos con formato legible
    print(json.dumps(datos, indent=4, ensure_ascii=False))

def obtenerMiUsuario():
    url = f'{host}/api/me?with=companies'
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Accept': 'application/json'
    }

    respuesta = rq.get(url, headers=headers)
    datos = controlErrores(respuesta)
    print(json.dumps(datos))

def borrarUusuario(nombreempresa, name, email, password):
    url = f'{host}/api/me?with=companies'
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
    datos = controlErrores(respuesta)
    print(json.dumps(datos))
