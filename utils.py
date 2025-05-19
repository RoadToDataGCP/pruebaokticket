import random
import time
import threading
from tqdm import tqdm
import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime

def obtenernameid(empresas):
    nombreid = list()
    for _, empresa in empresas.iterrows():
        nombreid1 = {
            'name': empresa["name"],
            'id': empresa["id"]
        }
        nombreid.append(nombreid1)
    return nombreid



def espera_con_barra(segundos: int, mensaje: str = "Esperando"):
    hilo = threading.current_thread().name
    for _ in tqdm(range(segundos), desc=f"⏳ {mensaje} - {hilo}", ncols=150):
        time.sleep(1)

def formato_hms(segundos):
    return time.strftime("%H:%M:%S", time.gmtime(segundos))

def obtener_ids_users_companies(token):
    
    load_dotenv()

    host = os.getenv("HOST")
    url = f"{host}/api/users?with=companies"

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error en la solicitud: {response.status_code}")

    data = response.json().get("data", [])
    resultado = []

    for usuario in data:
        companies = usuario.get("companies", [])
        for company in companies:
            pivot = company.get("pivot", {})
            id_user = pivot.get("id_user")
            id_company = pivot.get("id_company")
            if id_user is not None and id_company is not None:
                resultado.append({
                    "id_user": id_user,
                    "id_company": id_company
                })

    return resultado

def log_error(response_text, context="Error desconocido", payload=None):
    load_dotenv()
    ERROR_LOG_FILE = os.getenv("ERROR_LOG_FILE", "errores_gastos.log")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    separator = "=" * 80
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{separator}\n")
        f.write(f"[{now}] {context}\n")
        if payload:
            f.write("[Payload enviado]\n")
            f.write(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
        f.write("[Respuesta del servidor]\n")
        f.write(response_text.strip() + "\n\n")

