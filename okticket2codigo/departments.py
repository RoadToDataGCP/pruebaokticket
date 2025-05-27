from controlerrores import control_errores
import constantes
import requests as rq
import json
import os

def crear_deparments(name, idcompany):
    url=f'{os.getenv('HOST')}/api/departments'
    payload = json.dumps({
        'name': name,
        'company_id': idcompany
    })
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Content-Type': 'application/json'
    }
    response = rq.request('POST', url, headers=headers, data=payload)
    datos = control_errores(response)
    print(json.dumps(datos, indent=4, ensure_ascii=False))


def listado_total_deparments():
    url=f'{os.getenv('HOST')}/api/departments'

    payload = json.dumps({

    })
    headers = {
    'Authorization': f'Bearer {constantes.TOKEND}',
    'Content-Type': 'application/json'
    }

    response = rq.request('GET', url, headers=headers, data=payload)
    datos = control_errores(response)
    return datos