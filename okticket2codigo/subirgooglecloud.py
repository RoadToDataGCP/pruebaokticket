import datetime as dt
from google.cloud import storage
from google.cloud import bigquery

def subirabucket(archivo, nombrebucket):
    try: 
        destination_blob_name = f"output/{archivo.split('/')[-1]}"
        client = storage.Client()
        bucket = client.bucket(nombrebucket)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(archivo)

        print(f"Archivo subido a gs://{nombrebucket}/{destination_blob_name}")
        
    except Exception as e:
        print(f"Error al subir el csv al bucket{e}")
        
        
from google.cloud import bigquery
import csv

def creartablaBigQuery(archivocsv, carpetatabla, nombretabla):
    try:
        reftabla = f"r2d-interno-dev.{carpetatabla}.{nombretabla}"

        # Leer encabezados del CSV
        with open(archivocsv, newline='', encoding='utf-8') as archivo_csv:
            lector = csv.reader(archivo_csv)
            encabezados = next(lector)  # Primera fila

        # Crear el schema con todos los campos como STRING
        esquema = [bigquery.SchemaField(nombre.strip(), "STRING") for nombre in encabezados]

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=False,
            schema=esquema,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            field_delimiter=",",
            quote_character='"',
        )

        client = bigquery.Client()

        with open(archivocsv, "rb") as archivo:
            job = client.load_table_from_file(archivo, reftabla, job_config=job_config)
            job.result()
        
        print("CSV subido a la tabla de BigQuery con todos los campos como STRING.")
        
    except Exception as e:
        print(f"Error al subir el CSV a la tabla BigQuery: {e}")
