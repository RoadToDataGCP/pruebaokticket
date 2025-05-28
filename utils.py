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
from faker import Faker

fake = Faker()

def obtener_nameid(empresas):
    nombreid = list()
    for _, empresa in empresas.iterrows():
        nombreid1 = {
            'name': empresa["name"],
            'id': empresa["id"]
        }
        nombreid.append(nombreid1)
    return nombreid

def obtener_deptid_empid(departamentos):
    nombreid = list()
    for _, empresa in departamentos.iterrows():
        nombreid1 = {
            'id_dept': empresa["id"],
            'id_emp': empresa["company_id"]
        }
        nombreid.append(nombreid1)
    return nombreid

def espera_con_barra(segundos: int, mensaje: str = "Esperando"):
    hilo = threading.current_thread().name
    for _ in tqdm(range(segundos), desc=f"⏳ {mensaje} - {hilo}", ncols=150):
        time.sleep(1)

def obtener_userid_empresaid(usuarios):
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

# Función principal dummy: simula la creación de gasto y calcula huella
def crear_gasto_dummy():
    # Payload simulado (mismo formato que usaría en producción)
    payload = {
        "user_id": 195605,
        "company_id": 73413,
        "department_id": 1,
        "type_id": 0,
        "category_id": 0,
        "status_id": 1,
        "date": "2018-07-24 15:30:00",
        "amount": 0.4,
        "name": "Gijón - El Entrego",
        "custom_fields": { "Combustible": "gasoil", "Litros": 200 },
        "comments": "Viaje del trabajo a casa"
    }

    # Simulamos una respuesta como la del API real
    fake_api_response = {
        "data": {
            **payload,
            "source": "SOURCE_UNKNOWN",
            "created_by": 195606,
            "tax_model_id": 1,
            "currency": "EUR",
            "updated_at": "2025-05-27 10:40:06",
            "created_at": "2025-05-27 10:40:06",
            "_id": "68359686b395cfe6e8056bd7",
            "integrity_hash": "07f938f83227ec35cb2dd0e837db9bcb4d38813085e0dca800260b8944776f87",
            "id": "68359686b395cfe6e8056bd7"
        },
        "status": "ok"
    }

    print("✅ [DUMMY] Gasto simulado creado correctamente")

    # Llamada interna a la función auxiliar
    custom_fields = fake_api_response['data'].get('custom_fields', {})
    calcular_huella_carbono(custom_fields)

    return fake_api_response

# Función auxiliar: calcula la huella de carbono
def calcular_huella_carbono(custom_fields):
    combustible = custom_fields.get("Combustible", "").lower()
    litros = custom_fields.get("Litros", 0)

    # Factores de emisión (kg CO2e por litro)
    factores_emision = {
        "gasoil": 2.68,
        "gas": 2.35,
        "electrico": 0  # Ajusta si tienes un factor específico
    }

    if combustible in factores_emision:
        factor = factores_emision[combustible]
        huella = litros * factor
        return huella
    else:
        return None
# Función principal: crea el gasto y calcula la huella
def crear_gasto():
    api_url = f"{os.getenv('HOST')}/api/expenses"

    payload = {
        "user_id": 195605,
        "company_id": 73413,
        "department_id": 1,
        "type_id": 0,
        "category_id": 0,
        "status_id": 1,
        "date": "2018-07-24 15:30:00",
        "amount": 0.4,
        "name": "Gijón - El Entrego",
        "custom_fields": { "Combustible": "gasoil", "Litros": fake.random_int(min=100, max=300) },
        "comments": "Viaje del trabajo a casa"
    }

    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "ok":
            print("⚠️ Respuesta no OK del API")
            return

        gasto = data.get("data", {})
        custom_fields = gasto.get('custom_fields', {})
        company = gasto.get('company', {})
        license_info = company.get('license', {})
        user = gasto.get('user', {})

        litros = custom_fields.get("Litros", 0)
        huella = calcular_huella_carbono(custom_fields)
        huella_valor = round(huella, 2) if huella is not None else None

        fila_csv = {
            'data.id': gasto.get('id'),
            'data.user_id': gasto.get('user_id'),
            'data.company_id': gasto.get('company_id'),
            'data.department_id': gasto.get('department_id'),
            'data.type_id': gasto.get('type_id'),
            'data.category_id': gasto.get('category_id'),
            'data.status_id': gasto.get('status_id'),
            'data.date': gasto.get('date'),
            'data.amount': gasto.get('amount'),
            'data.name': gasto.get('name'),
            'data.custom_fields.Combustible': custom_fields.get('Combustible'),
            'data.custom_fields.Litros': litros,
            'huella_carbono': huella_valor,
            'data.comments': gasto.get('comments'),
            'data.source': gasto.get('source'),
            'data.updated_at': gasto.get('updated_at'),
            'data.created_at': gasto.get('created_at'),
            'data._id': gasto.get('_id'),
            'data.integrity_hash': gasto.get('integrity_hash'),
            'data.company.id': company.get('id'),
            'data.company.name': company.get('name'),
            'data.company.cif': company.get('cif'),
            'data.company.fiscal_address': company.get('fiscal_address'),
            'data.company.city': company.get('city'),
            'data.company.contact_number': company.get('contact_number'),
            'data.company.license_id': company.get('license_id'),
            'data.company.company_size': company.get('company_size'),
            'data.company.verify_image_token': company.get('verify_image_token'),
            'data.company.country_id': company.get('country_id'),
            'data.company.currency': company.get('currency'),
            'data.company.distance_unit_price': company.get('distance_unit_price'),
            'data.company.okt_card_provider_token': company.get('okt_card_provider_bussiness_token'),
            'data.company.group_id': company.get('group_id'),
            'data.company.custom_id': company.get('custom_id'),
            'data.company.license.id': license_info.get('id'),
            'data.company.license.updated_at': license_info.get('updated_at'),
            'data.company.license.deleted_at': license_info.get('deleted_at'),
            'data.user.id': user.get('id'),
            'data.user.name': user.get('name'),
            'data.user.email': user.get('email'),
            'data.user.id_role': user.get('id_role'),
            'data.user.status_id': user.get('status_id'),
            'data.user.company_type_id': user.get('company_type_id'),
            'data.user.updated_at': user.get('updated_at'),
            'data.user.deleted_at': user.get('deleted_at'),
            'data.user.active_company': user.get('active_company'),
            'data.user.active_department': user.get('active_department'),
            'data.user.custom_id': user.get('custom_id'),
            'data.user.custom_id_2': user.get('custom_id_2'),
            'data.user.custom_id_3': user.get('custom_id_3')            
        }

        encabezados_csv = list(fila_csv.keys())
        guardar_en_csv("gastos.csv", fila_csv, encabezados_csv)

        print(f"✅ Gasto creado correctamente con ID: {gasto.get('_id')}")
        if huella_valor is not None:
            print(f"✅ Huella de carbono que emitirá: {huella_valor} kg CO2e")
        print("✅ Datos guardados en gastos.csv")

        return data

    except requests.exceptions.HTTPError as errh:
        print("❌ Error HTTP:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("❌ Error de conexión:", errc)
    except requests.exceptions.Timeout as errt:
        print("❌ Timeout:", errt)
    except requests.exceptions.RequestException as err:
        print("❌ Error general:", err)

    return None
# Función principal: pide company_id, obtiene gastos, calcula y muestra huella
def cargar_csv_en_diccionario(nombre_archivo, clave_id="_id"):
    datos = {}
    if not os.path.isfile(nombre_archivo):
        return datos

    with open(nombre_archivo, mode='r', newline='', encoding='utf-8') as archivo_csv:
        reader = csv.DictReader(archivo_csv)
        for fila in reader:
            datos[fila.get(clave_id)] = fila
    return datos

def guardar_diccionario_en_csv(nombre_archivo, datos_diccionario, encabezados):
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
        writer = csv.DictWriter(archivo_csv, fieldnames=encabezados)
        writer.writeheader()
        for fila in datos_diccionario.values():
            writer.writerow(fila)

def obtener_y_calcular_huella():
    company_input = input("Introduce el company_id (o deja vacío para todos): ").strip()

    base_url = f"{os.getenv('HOST')}/api/expenses"
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Content-Type': 'application/json'
    }
    params = {}

    if company_input != "":
        try:
            company_id = int(company_input)
            params["company"] = company_id
        except ValueError:
            print("❌ El company_id debe ser un número entero.")
            return

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            print("⚠️ Respuesta no OK del API")
            return

        gastos = data.get("data", [])
        if not gastos:
            print("ℹ️ No se encontraron gastos.")
            return

        csv_archivo = "gastos.csv"
        registros_csv = cargar_csv_en_diccionario(csv_archivo, clave_id="data._id")

        encabezados = [
            'data.id', 'data.user_id', 'data.company_id', 'data.department_id', 'data.type_id',
            'data.category_id', 'data.status_id', 'data.date', 'data.amount', 'data.name',
            'data.custom_fields.Combustible', 'data.custom_fields.Litros', 'huella_carbono',
            'data.comments', 'data.source', 'data.updated_at', 'data.created_at', 'data._id',
            'data.integrity_hash',
            'data.company.id', 'data.company.name', 'data.company.cif', 'data.company.fiscal_address',
            'data.company.city', 'data.company.contact_number', 'data.company.license_id',
            'data.company.company_size', 'data.company.verify_image_token', 'data.company.country_id',
            'data.company.currency', 'data.company.distance_unit_price', 'data.company.okt_card_provider_token',
            'data.company.group_id', 'data.company.custom_id', 'data.company.license.id',
            'data.company.license.updated_at', 'data.company.license.deleted_at',
            'data.user.id', 'data.user.name', 'data.user.email', 'data.user.id_role',
            'data.user.status_id', 'data.user.company_type_id', 'data.user.updated_at',
            'data.user.deleted_at', 'data.user.active_company', 'data.user.active_department',
            'data.user.custom_id', 'data.user.custom_id_2', 'data.user.custom_id_3'
        ]

        for gasto in gastos:
            # Extraemos sub-objetos company, user, license_info con fallback a dict vacía
            company = gasto.get('company', {})
            user = gasto.get('user', {})
            license_info = company.get('license', {})

            custom_fields = gasto.get('custom_fields', {})
            litros = custom_fields.get('Litros', 0)

            huella = calcular_huella_carbono(custom_fields)
            huella_valor = round(huella, 2) if huella is not None else ""

            expense_id = gasto.get('_id')

            fila_csv = {
                'data.id': gasto.get('id'),
                'data.user_id': gasto.get('user_id'),
                'data.company_id': gasto.get('company_id'),
                'data.department_id': gasto.get('department_id'),
                'data.type_id': gasto.get('type_id'),
                'data.category_id': gasto.get('category_id'),
                'data.status_id': gasto.get('status_id'),
                'data.date': gasto.get('date'),
                'data.amount': gasto.get('amount'),
                'data.name': gasto.get('name'),
                'data.custom_fields.Combustible': custom_fields.get('Combustible'),
                'data.custom_fields.Litros': litros,
                'huella_carbono': huella_valor,
                'data.comments': gasto.get('comments'),
                'data.source': gasto.get('source'),
                'data.updated_at': gasto.get('updated_at'),
                'data.created_at': gasto.get('created_at'),
                'data._id': expense_id,
                'data.integrity_hash': gasto.get('integrity_hash'),
                'data.company.id': company.get('id'),
                'data.company.name': company.get('name'),
                'data.company.cif': company.get('cif'),
                'data.company.fiscal_address': company.get('fiscal_address'),
                'data.company.city': company.get('city'),
                'data.company.contact_number': company.get('contact_number'),
                'data.company.license_id': company.get('license_id'),
                'data.company.company_size': company.get('company_size'),
                'data.company.verify_image_token': company.get('verify_image_token'),
                'data.company.country_id': company.get('country_id'),
                'data.company.currency': company.get('currency'),
                'data.company.distance_unit_price': company.get('distance_unit_price'),
                'data.company.okt_card_provider_token': company.get('okt_card_provider_bussiness_token'),
                'data.company.group_id': company.get('group_id'),
                'data.company.custom_id': company.get('custom_id'),
                'data.company.license.id': license_info.get('id'),
                'data.company.license.updated_at': license_info.get('updated_at'),
                'data.company.license.deleted_at': license_info.get('deleted_at'),
                'data.user.id': user.get('id'),
                'data.user.name': user.get('name'),
                'data.user.email': user.get('email'),
                'data.user.id_role': user.get('id_role'),
                'data.user.status_id': user.get('status_id'),
                'data.user.company_type_id': user.get('company_type_id'),
                'data.user.updated_at': user.get('updated_at'),
                'data.user.deleted_at': user.get('deleted_at'),
                'data.user.active_company': user.get('active_company'),
                'data.user.active_department': user.get('active_department'),
                'data.user.custom_id': user.get('custom_id'),
                'data.user.custom_id_2': user.get('custom_id_2'),
                'data.user.custom_id_3': user.get('custom_id_3')
            }

            if expense_id in registros_csv:
                fila_existente = registros_csv[expense_id]
                actualizado = False

                for key in encabezados:
                    # Si el valor está vacío o None, lo actualizamos con el nuevo dato si existe
                    if (not fila_existente.get(key) or fila_existente.get(key) in ["", "0", None]) and fila_csv.get(key):
                        fila_existente[key] = fila_csv[key]
                        actualizado = True

                if actualizado:
                    print(f"✅ CSV actualizado para Expense ID: {expense_id}")
                else:
                    print(f"ℹ️ Sin cambios necesarios para Expense ID: {expense_id}")

            else:
                # Añadimos fila nueva
                registros_csv[expense_id] = fila_csv
                print(f"➕ Nuevo gasto añadido al CSV: Expense ID {expense_id}")

        if registros_csv:
            guardar_diccionario_en_csv(csv_archivo, registros_csv, encabezados)
            print(f"✅ CSV {csv_archivo} guardado con todas las actualizaciones y añadidos.")

            # Borramos el CSV al final, según lo solicitado
            os.remove(csv_archivo)
            print(f"🗑️ CSV {csv_archivo} eliminado tras la operación.")

        print("✅ Cálculo, actualización y limpieza completados.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la solicitud: {e}")
    except Exception as ex:
        print(f"❌ Error inesperado: {ex}")
def guardar_en_csv(nombre_archivo, datos, encabezados):
    archivo_existe = os.path.isfile(nombre_archivo)
    with open(nombre_archivo, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=encabezados)
        if not archivo_existe:
            writer.writeheader()
        writer.writerow(datos)