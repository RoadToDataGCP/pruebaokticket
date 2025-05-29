import datetime as dt
from google.cloud import storage
from google.cloud import bigquery

def subirabucket(archivo, nombrebucket):
    try: 
        fechahoy = dt.datetime.now().strftime("%Y-%m-%d")
        destination_blob_name = f"csv/{archivo.split('/')[-1]}"

        client = storage.Client()
        bucket = client.bucket(nombrebucket)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(archivo)

        print(f"Archivo subido a gs://{nombrebucket}/{destination_blob_name}")
        
    except Exception as e:
        print(f"Error al subir el csv al bucket{e}")
        
        
def creartablaBigQuery(archivocsv, carpetatabla, nombretabla):
    try:
        reftabla = f"r2d-interno-dev.{carpetatabla}.{nombretabla}"

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=False,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            schema_update_options=[],
            field_delimiter=",",
            quote_character='"',
        )

        client = bigquery.Client()

        with open(archivocsv, "rb") as archivo:
            job = client.load_table_from_file(archivo, reftabla, job_config=job_config)
            job.result()
        
        print("Csv subido a la tabla de big query")
        
    except Exception as e:
        print(f"Error al subir el csv a la tabla big query: {e}")