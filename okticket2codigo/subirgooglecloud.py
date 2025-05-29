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
        
        
def creartablaBigQuery(archivocsv, carpetatabla, nombretabla):
    try:
        client = bigquery.Client()
        reftabla = f"r2d-interno-dev.{carpetatabla}.{nombretabla}"
        dataset_ref = client.dataset(carpetatabla)
        table_ref = dataset_ref.table(nombretabla)

        with open(archivocsv, "r", encoding="utf-8") as archivo_texto:
            primera_linea = archivo_texto.readline()
            encabezados = [col.strip() for col in primera_linea.strip().split(",")]

        esquema = [bigquery.SchemaField(nombre, "STRING") for nombre in encabezados]

        try:
            client.get_table(table_ref)
            print(f"La tabla {reftabla} ya existe. Se truncará al cargar.")
        except Exception:
            print(f"La tabla {reftabla} no existe. Creándola...")
            tabla = bigquery.Table(table_ref, schema=esquema)
            client.create_table(tabla)
            print("Tabla creada correctamente.")

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=False,
            schema=esquema,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            field_delimiter=",",
            quote_character='"',
        )

        with open(archivocsv, "rb") as archivo:
            job = client.load_table_from_file(archivo, reftabla, job_config=job_config)
            job.result()
        
        print("CSV subido a la tabla de BigQuery con todos los campos como STRING.")
        
    except Exception as e:
        print(f"Error al subir el CSV a la tabla BigQuery: {e}")