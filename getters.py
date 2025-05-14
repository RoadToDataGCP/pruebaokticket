import requests
from dotenv import load_dotenv
import os
import json

def get_users(token, empresa):
    load_dotenv()

    host = os.getenv("HOST")
    url = f"{host}/api/users?with=companies"

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'company': empresa
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    # Imprime solo la lista de usuarios (clientes)
    print(json.dumps(data.get("data", []), indent=4, ensure_ascii=False))

def get_users_companies_summary(token, empresa):
    load_dotenv()

    host = os.getenv("HOST")
    url = f"{host}/api/users?with=companies"

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'company': empresa
    }

    response = requests.get(url, headers=headers)
    users = response.json().get("data", [])

    resumen = []

    for user in users:
        user_info = {
            "user_name": user.get("name"),
            "user_email": user.get("email"),
            "user_distance_unit_price": user.get("distance_unit_price"),
            "companies": []
        }

        for company in user.get("companies", []):
            company_info = {
                "company_name": company.get("name"),
                "cif": company.get("cif"),
                "contact_number": company.get("contact_number"),
                "contact_email": company.get("contact_email")
            }
            user_info["companies"].append(company_info)

        resumen.append(user_info)

    print(json.dumps(resumen, indent=4, ensure_ascii=False))


def get_companies(token):
    load_dotenv()

    url = f"{os.getenv('HOST')}/api/companies"

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        companies = response.json().get("data", [])
        print(json.dumps(companies, indent=4, ensure_ascii=False))
    else:
        print("Error al obtener las empresas:")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))

def get_companies_filtered(token):
    load_dotenv()

    url = f"{os.getenv('HOST')}/api/companies"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        companies = response.json().get("data", [])

        filtered = []
        for company in companies:
            filtered.append({
                "name": company.get("name"),
                "cif": company.get("cif"),
                "fiscal_address": company.get("fiscal_address"),
                "postal_code": company.get("postal_code"),
                "city": company.get("city"),
                "logo_path": company.get("logo_path"),
                "contact_number": company.get("contact_number"),
                "contact_email": company.get("contact_email")
            })

        print(json.dumps(filtered, indent=4, ensure_ascii=False))
    else:
        print("Error al obtener las empresas:")
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))

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

