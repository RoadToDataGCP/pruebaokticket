import random
import pandas as pd
import constantes
import time
import threading
from tqdm import tqdm
import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import csv
from google.cloud import storage
from google.cloud import bigquery
import logging

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

def obteneruseridempresaid(usuarios):
    useridempid = list()
    listausuarios= usuarios['data']
    for user in listausuarios:
        useidempid1 = dict()
        useidempid1['iduser'] = user['id']
        listaemp =  user['companies']
        for emp in listaemp:
            useidempid1['idemp'] = emp['id']
        useridempid.append(useidempid1)
    return useridempid


def crearCsvUsuarios(datos):
    datos = datos['data']
    listausuarios = list()
    for user in datos:
        #companies = user.get("companies", [])
        #company_id = companies[0]["id"] if companies else None  # Evita el error
        fila = {
            'id' : user['id'] , 
            'name': user['name'], 
            'email': user['email'], 
            'id_role': user['id_role'] , 
            'status_id': user['status_id'], 
            'company_type_id': user['company_type_id'],
            'currency': user['currency'], 
            'app_version': user['app_version'], 
            'legal_texts_version': user[ 'legal_texts_version'],
            'pop_checked': user['pop_checked'],
            'tyc_checked': user['tyc_checked'],
            'created_at': user['created_at'],
            'updated_at': user['updated_at'],
            'deleted_at': user['deleted_at'],
            'active_company': user['active_company'],
            'active_department': user['active_department'],
            'custom_id': user['custom_id'],
            'custom_id_2': user['custom_id_2'],
            'custom_id_3': user['custom_id_3'],
            'language': user['language'],
            'active': user['active'],
            'last_login_date': user['last_login_date'],
            'login_error_count': user['login_error_count'],
            'skip_sso': user['skip_sso'],
            'companies' : user["companies"][0]["id"] 
        }
        listausuarios.append(fila)
    csvususarios = pd.DataFrame(listausuarios)
    csvususarios.to_csv("usuarios.csv", mode="w", header=constantes.CABECERAUSUARIOS, index=False)
    return csvususarios
        
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
def subir_a_bucket(csv_file_local, bucket_name,bucket_csv):

    today_date = datetime.now().strftime("%Y-%m-%d")
    # Crear la ruta de destino en el bucket
    # usando la fecha actual
    # y el nombre del archivo local
    # para evitar conflictos de nombres
    # y mantener la organización
    # de los archivos en el bucket
    destination_blob_name = f"{bucket_csv}/{today_date}/{csv_file_local.split('/')[-1]}"

    # Crear el cliente de Google Cloud Storage
    # y subir el archivo CSV
    # al bucket especificado
    # usando la ruta de destino creada
    # y el nombre del archivo local
    # para evitar conflictos de nombres
    # y mantener la organización
    # de los archivos en el bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(csv_file_local)

    print(f"🔄 Archivos subidos a gs://{bucket_name}/{destination_blob_name}")

    # Función para cargar el CSV en BigQuery
def cargar_csv_a_bigquery(client, csv_path, project_id, dataset_id, table_id):
    # Cargar el CSV en BigQuery
    # usando el cliente de BigQuery
    # y el ID del proyecto, dataset y tabla
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    
    # Configurar el trabajo de carga
    # especificando el formato de origen, la configuración de escritura
    # y las opciones de actualización del esquema
    # para evitar conflictos de datos
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=False,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        schema_update_options=[],
        field_delimiter=",",
        quote_character='"',
    )

    # Leer los encabezados del CSV y reemplazar guiones por guiones bajos
    with open(csv_path, 'r', encoding='utf-8') as f:
        headers = f.readline().strip().split(',')
    
    # Reemplazar los guiones por guiones bajos en los nombres de las columnas
    headers = [header.replace('-', '_') for header in headers]

    # Crear un archivo temporal con la columna 'fecha_carga' añadida
    tmp_path = "tmp_bq_upload.csv"
    with open(tmp_path, 'w', encoding='utf-8') as fout:
        with open(csv_path, 'r', encoding='utf-8') as fin:
            for i, line in enumerate(fin):
                line = line.strip()
                if i == 0:
                    fout.write(f"{','.join(headers)}\n")
                else:
                    fout.write(f"{line}\n")

    # Subir el archivo CSV modificado a BigQuery
    with open(tmp_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
        job.result()

    # Eliminar el archivo temporal
    os.remove(tmp_path)

    logging.info(f"✅ Carga completada: {len(headers)} columnas + campo 'fecha_carga' en '{table_ref}'.")

# Función para comprobar si el archivo CSV no está vacío
def verificar_csv_no_vacio(csv_path):
    # Comprobar si el archivo CSV existe y no está vacío
    if os.path.isfile(csv_path) and os.path.getsize(csv_path) > 0:
        logging.info(f"📄 El CSV '{csv_path}' existe y no está vacío.")
        return True
    else:
        logging.error(f"❌ El archivo CSV '{csv_path}' está vacío o no existe.")
        return False

# Función para verificar si la tabla existe en BigQuery
def tabla_existe(client, project_id, dataset_id, table_id):
    # Comprobar si la tabla existe en BigQuery
    # usando el cliente de BigQuery
    # y el ID del proyecto, dataset y tabla
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    try:
        client.get_table(table_ref)
        logging.info(f"📊 La tabla '{table_ref}' existe en BigQuery.")
        return True
    except Exception as e:
        logging.error(f"❌ No se encontró la tabla '{table_ref}': {e}")
        return False

# Función para borrar los datos existentes en la tabla de BigQuery
def borrar_datos_tabla(client, project_id, dataset_id, table_id):
    # Borrar los datos existentes en la tabla de BigQuery
    # usando el cliente de BigQuery
    # y el ID del proyecto, dataset y tabla
    # para evitar conflictos de datos
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    query = f"DELETE FROM `{table_ref}` WHERE TRUE"
    client.query(query).result()
    logging.info(f"🗑️ Se han borrado los datos existentes en la tabla '{table_ref}'.")


# Función principal para automatizar la carga de datos a BigQuery
# y manejar errores, reintentos, logging y limitación de tasa
def automatizar_carga_bigquery(csv_path, project_id, dataset_id, table_id):
    logging.info("🚀 Iniciando proceso de carga de datos a BigQuery...")

    # Comprobar si el archivo CSV no está vacío
    if not verificar_csv_no_vacio(csv_path):
        return

    # Configurar el cliente de BigQuery
    client = bigquery.Client()

    # Comprobar si la tabla existe en BigQuery
    if not tabla_existe(client, project_id, dataset_id, table_id):
        return

    # Borrar los datos existentes en la tabla de BigQuery
    borrar_datos_tabla(client, project_id, dataset_id, table_id)

    # Cargar el CSV en BigQuery
    cargar_csv_a_bigquery(client, csv_path, project_id, dataset_id, table_id)

    logging.info("🎯 Proceso finalizado correctamente.")

