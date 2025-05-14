import requests
from dotenv import load_dotenv
import os
import json
import datetime

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

def create_gasto(token):
    load_dotenv()

    url = f"{os.getenv('HOST')}/api/expenses"

    user_id = input("👉 Ingresa el ID del usuario: ").strip()
    company_id = input("👉 Ingresa el ID de la empresa: ").strip()
    department_id = input("👉 Ingresa el ID del departamento: ").strip()
    type_id = input("👉 Ingresa el ID del tipo de gasto, 0 (ticket), 1 (factura), 2 (kilometraje), 4 (dieta): ").strip()
    category_id = input("👉 Ingresa el ID de la categoría: ").strip()
    date = input("👉 Ingresa la fecha (YYYY-MM-DD HH:MM:SS): ").strip()
    amount = input("👉 Ingresa el importe: ").strip()
    name = input("👉 Ingresa el nombre: ").strip()
    comments = input("👉 Ingresa los comentarios: ").strip()

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
    headers = {
      'Authorization': f'Bearer {token}',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

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
