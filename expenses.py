import requests
from dotenv import load_dotenv
import os
import json
import datetime
from faker import Faker
import random
from datetime import datetime

def get_gastos_by_empresa(token, empresa):
    load_dotenv()

    url = f"{os.getenv('HOST')}/api/expenses?with=companies"

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'company': empresa
    }

    response = requests.get(url, headers=headers)

    try:
        gastos = response.json()
        print(json.dumps(gastos, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print("⚠️ Error: La respuesta no es un JSON válido")
        print(response.text)

def get_gastos_by_date(token, fecha):
    load_dotenv()

    fecha = input("👉 Ingresa la fecha (YYYY-MM-DD): ").strip()

    # Convertir la fecha a formato ISO 8601
    fecha_iso = datetime.strptime(fecha, "%Y-%m-%d").isoformat()

    url = f"{os.getenv('HOST')}/api/expenses?&updated_after={fecha_iso}&paginate=false"

    payload={}
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    try:
        gastos = response.json()
        print(json.dumps(gastos, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print("⚠️ Error: La respuesta no es un JSON válido")
        print(response.text)



def create_gasto(token, company_id):
    load_dotenv()
    fake = Faker('es_ES')  # Localización en español

    url = f"{os.getenv('HOST')}/api/expenses"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Simulación de datos
    user_id = str(random.randint(1000, 9999)) #Cambiar por un ID de usuario real, buscar a traves de la API.
    department_id = str(random.randint(10, 99))
    type_id = str(random.choice([0, 1, 2, 4]))
    category_id = str(random.randint(1, 20))  # Asumimos que hay 20 categorías

    # Fecha en los últimos 30 días
    date = fake.date_time_between(start_date='-30d', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
    amount = round(random.uniform(10.00, 500.00), 2)  # Importe entre 10€ y 500€
    name = fake.sentence(nb_words=3).rstrip('.')  # Nombre corto
    comments = fake.text(max_nb_chars=100)

    payload = json.dumps({
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
    })

    response = requests.post(url, headers=headers, data=payload)

    try:
        gastos = response.json()
        print(json.dumps(gastos, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print("⚠️ Error: La respuesta no es un JSON válido")
        print(response.text)



def get_gasto_by_id(token, gasto_id):
    load_dotenv()
    url = f"{os.getenv('HOST')}/api/expenses/{gasto_id}?with=report"

    payload={}
    headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    try:
        gastos = response.json()
        print(json.dumps(gastos, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print("⚠️ Error: La respuesta no es un JSON válido")
        print(response.text)
