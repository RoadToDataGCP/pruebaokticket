from controlerrores import control_errores
import constantes
import requests as rq
import json
import os

def crear_user(name_company, name, email, password, ids_companies, custom_id, custom_id2, custom_id3):
    url = f"{os.getenv('HOST')}/api/users"
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'company': name_company
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
    # Imprimir datos
    print(json.dumps(datos, indent=4, ensure_ascii=False))

def listado_total_users():

    url = f"{os.getenv('HOST')}/api/users?with=companies"
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    respuesta = rq.get(url, headers=headers)
    datos = control_errores(respuesta)
    # Imprimir datos con formato legible
    return datos

def listado_users_de_una_company(idcompay):
  url = f"{os.getenv('HOST')}/api/companies/{idcompay}/users"
  headers = {
      'Authorization': f'Bearer {constantes.TOKEND}',
      'Accept': 'application/json',
      'Content-Type': 'application/json',
  }

  respuesta = rq.get(url, headers=headers)
  datos = control_errores(respuesta)
  return datos

def asociar_user_a_department(iduser,emailuser, idcompany, iddept):
    url = f"{os.getenv('HOST')}/api/users/{iduser}"
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
    }
    payload = {
        'email': emailuser,
        'ids_companies': {
            idcompany: {
                'id_role': 2
            }	
        },
        'ids_departments': {
            iddept: {
                'id_role': 3
            }
        }
    }

    respuesta = rq.patch(url, headers=headers, json=payload)
    datos = control_errores(respuesta)
    # Imprimir datos con formato legible
    print(json.dumps(datos, indent=4, ensure_ascii=False))

