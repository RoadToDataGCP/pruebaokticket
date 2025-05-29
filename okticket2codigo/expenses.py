import requests
import os
import json
import random
from controlerrores import control_errores
import constantes


def crear_expenses(id_company, id_user, date, amount, name, comments):
    url = f"{os.getenv('HOST')}/api/expenses"

    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Content-Type': 'application/json'
    }

    department_id = str(random.randint(10, 99))
    type_id = str(random.choice([0, 1, 2, 4]))
    category_id = str(random.randint(1, 20))

    payload = {
        "user_id": id_user,
        "company_id": id_company,
        "department_id": department_id,
        "type_id": type_id,
        "category_id": category_id,
        "status_id": 0,
        "date": date,
        "amount": amount,
        "name": name,
        "comments": comments
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    datos = control_errores(response)
    print(json.dumps(datos, indent=4, ensure_ascii=False))


def listado_total_expenses():
    url = f"{os.getenv('HOST')}/api/expenses"

    payload={}
    headers = {
    'Authorization': f'Bearer {constantes.TOKEND}',
    'Accept': 'application/json'
    }

    response = requests.request('GET', url, headers=headers, data=payload)
    datos = control_errores(response)
    return datos