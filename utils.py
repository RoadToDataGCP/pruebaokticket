import os
import json
from datetime import datetime
import csv
import logging


def obtener_nameid(empresas):
    nombreid = list()
    for _, empresa in empresas.iterrows():
        nombreid1 = {
            'name': empresa["name"],
            'id': empresa["id"]
        }
        nombreid.append(nombreid1)
    return nombreid


def obtener_userid_empresaid(usuarios):
    useridempid = list()
    listausuarios= usuarios['data']
    for user in listausuarios:
        useidempid1 = dict()
        iduser = user['id']
        listaemp =  user['companies']
        for emp in listaemp:
              useidempid1 = {
                'iduser': iduser,
                'idemp': emp['id']
              }
        useridempid.append(useidempid1)
    return useridempid
        

def log_error(response_text, context="Error desconocido", payload=None):
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

def calcular_huella_carbono(distancia, litros):
    # Definición de la huella de carbono por litro de combustible
    emisiones_por_litro = 2.486  # kg CO2 por litro

    # Cálculo de la huella de carbono total
    emisiones_totales = litros * emisiones_por_litro

    huella_total = distancia * emisiones_totales #Asumiendo conocer el consumo de combustible

    huella_total = (distancia * emisiones_por_litro) * 0.1  #Asumiendo un consumo de 10L/100km

    huella_total = round(huella_total, 2)
    print(f"Huella de carbono total: {huella_total} kg CO2")

def convertir_json_a_csv_expenses(json_file, csv_file):
    # Cargar el JSON desde el archivo
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Acceder a la lista de datos dentro de la clave "data"
    data = json_data

    if not data:
        print("No hay registros en la clave 'data'.")
        return

    # Obtener todas las claves únicas de los elementos de data para usarlas como encabezado
    header = sorted({key for item in data for key in item.keys()})

    # Escribir el CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

    print("El archivo JSON se ha convertido correctamente a CSV.")

# Función para subir un archivo CSV a Google Cloud Storage

# Función para comprobar si el archivo CSV no está vacío
def verificar_csv_no_vacio(csv_path):
    # Comprobar si el archivo CSV existe y no está vacío
    if os.path.isfile(csv_path) and os.path.getsize(csv_path) > 0:
        logging.info(f"📄 El CSV '{csv_path}' existe y no está vacío.")
        return True
    else:
        logging.error(f"❌ El archivo CSV '{csv_path}' está vacío o no existe.")
        return False
