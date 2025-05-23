import requests
import os
import json
import datetime
from faker import Faker
import random
from datetime import datetime
from utils import log_error
from controlerrores import control_errores
import constantes

def guardar_gasto_en_json(gasto):
    fecha = datetime.now().strftime("%Y%m%d")
    filename = f"expenses_{fecha}.json"

    # Si existe, lo carga; si no, empieza una lista vacía
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(gasto)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def create_gasto( company_id, user_id):
    fake = Faker('es_ES')
    url = f'{os.getenv('HOST')}/api/expenses'
    
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Content-Type': 'application/json'
    }

    department_id = str(random.randint(10, 99))
    type_id = str(random.choice([0, 1, 2, 4]))
    category_id = str(random.randint(1, 20))

    date = fake.date_time_between(start_date='-30d', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
    amount = round(random.uniform(10.00, 500.00), 2)
    name = fake.sentence(nb_words=3).rstrip('.')
    comments = fake.text(max_nb_chars=100)

    payload = {
        "user_id": user_id,
        "company_id": company_id,
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

    try:
        data = response.json()["data"]
        # Guardar el gasto completo en el JSON
        guardar_gasto_en_json(data)

    except json.JSONDecodeError:
        context = "⚠️ Error: Respuesta no es un JSON válido"
        log_error(response.text, context, payload)

    except KeyError as e:
        context = f"⚠️ Error: Campo faltante en JSON → {str(e)}"
        log_error(response.text, context, payload)

#NO SE UTILIZA
def obtener_gastos_por_id( gasto_id):
    url = f'{os.getenv('HOST')}/api/expenses/{gasto_id}?with=report'
    payload={}
    headers = {
    'Authorization': f'Bearer {constantes.TOKEND}',
    'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    try:
        gastos = control_errores(response)
        print(json.dumps(gastos, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print("⚠️ Error: La respuesta no es un JSON válido")
        print(response.text)

def obtener_gastos_por_empresa(empresa):
    url = f'{os.getenv('HOST')}/api/expenses?with=companies'

    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Accept': 'application/json',
        'company': empresa
    }

    response = requests.get(url, headers=headers)

    try:
        datos = control_errores(response)
        print(json.dumps(datos, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print("⚠️ Error: La respuesta no es un JSON válido")
        print(response.text)

def obtener_gastos_por_fecha(fecha):
    fecha = input("👉 Ingresa la fecha (YYYY-MM-DD): ").strip()
    # Convertir la fecha a formato ISO 8601
    fecha_iso = datetime.strptime(fecha, "%Y-%m-%d").isoformat()

    url = f'{os.getenv('HOST')}/api/expenses?&updated_after={fecha_iso}&paginate=false'
    payload={}
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    try:
        gastos = control_errores(response)
        print(json.dumps(gastos, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print("⚠️ Error: La respuesta no es un JSON válido")
        print(response.text)
