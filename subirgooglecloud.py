
import os
from datetime import datetime
from google.cloud import storage
from google.cloud import bigquery
import logging
from utils import verificar_csv_no_vacio

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