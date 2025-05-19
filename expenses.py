import requests
from dotenv import load_dotenv
import os
import json
import datetime
from faker import Faker
import random
from datetime import datetime
from rich import print as rprint  # Necesitas instalar la librería `rich`
from rich.panel import Panel
from rich.table import Table
from utils import log_error

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

def create_gasto(token, company_id, user_id):
    load_dotenv()
    fake = Faker('es_ES')
    url = f"{os.getenv('HOST')}/api/expenses"
    
    headers = {
        'Authorization': f'Bearer {token}',
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

        company_name = data["company"]["name"]
        user_name = data["user"]["name"]
        table = Table(title="✅ Gasto creado correctamente")

        table.add_column("Campo", style="bold cyan")
        table.add_column("Valor", style="green")

        table.add_row("Usuario", user_name)
        table.add_row("ID Usuario", str(data["user_id"]))
        table.add_row("Empresa", company_name)
        table.add_row("ID Empresa", str(data["company_id"]))
        table.add_row("Nombre gasto", data["name"])
        table.add_row("Fecha", data["date"])
        table.add_row("Importe", f"{data['amount']} €")
        table.add_row("Categoría ID", str(data["category_id"]))
        table.add_row("Comentario", data["comments"][:50] + ("..." if len(data["comments"]) > 50 else ""))

        rprint(table)

        # Guardar el gasto completo en el JSON
        guardar_gasto_en_json(data)

    except json.JSONDecodeError:
        context = "⚠️ Error: Respuesta no es un JSON válido"
        rprint(Panel.fit(
            f"[red bold]{context}[/red bold]\n[white]Guardado en '{os.getenv('ERROR_LOG_FILE', 'errores_gastos.log')}'[/white]",
            title="Respuesta inválida"
        ))
        log_error(response.text, context, payload)

    except KeyError as e:
        context = f"⚠️ Error: Campo faltante en JSON → {str(e)}"
        rprint(Panel.fit(
            f"[red bold]{context}[/red bold]\n[white]Guardado en '{os.getenv('ERROR_LOG_FILE', 'errores_gastos.log')}'[/white]",
            title="Error de formato"
        ))
        log_error(response.text, context, payload)

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

