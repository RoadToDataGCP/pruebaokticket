from faker import Faker
from obtenertoken import obtener_tokend
from empresa import crear_empresa, ver_empresas
from users import create_user, obtener_lista_total_usuarios, crear_csv_usuarios
from expenses import create_gasto
from utils import obtener_nameid, obtener_userid_empresaid, convertir_json_a_csv_expenses
from subirgooglecloud import subir_a_bucket, automatizar_carga_bigquery 
from datetime import datetime
from dotenv import load_dotenv

def main():

    # Crear una instancia de Faker
    fake = Faker()

    # Obtener tocken 
    obtener_tokend()

    

    #Obtener lista de empresas
    empresas = ver_empresas()
    nameid = obtener_nameid(empresas)

    for empresa in nameid:
        name = empresa["name"]
        company_id = empresa["id"]
        for _ in range(3):
            print(f"Creando usuario para la empresa {name} con ID {company_id}")
            # Crear usuario
            create_user(name, fake.name(), fake.email(), fake.password(), [company_id] , "1234", "1234", "1234")

    #Obtener lista de usuarios
    usuarios = obtener_lista_total_usuarios()
    crear_csv_usuarios(usuarios) #Crear CSV de usuarios
    relaciones = obtener_userid_empresaid(usuarios)
    
    for relacion in relaciones:
        user_id = relacion["iduser"]
        company_id = relacion["idemp"]
        print(f"Creando gasto para la empresa con ID {company_id} y usuario {user_id}")
        # Crear gasto
        create_gasto(company_id, user_id)

    #Conversion de json de gastos a csv
    fecha = datetime.now().strftime("%Y%m%d")
    filename = f"expenses_{fecha}.json"
    csv_file = f"expenses.csv"
    convertir_json_a_csv_expenses(filename, csv_file)

def subir_expenses():
    #Conversion de json de gastos a csv
    fecha = datetime.now().strftime("%Y%m%d")
    filename = f"expenses_{fecha}.json"
    csv_file = f"expenses.csv"
    convertir_json_a_csv_expenses(filename, csv_file)

    #Subir a bucket
    bucket_name = "prueba-okticket"
    bucket_csv = "bucket-gastos"
    subir_a_bucket(csv_file, bucket_name,bucket_csv)
    print(f"Archivo {filename} subido a {bucket_name}.")

    automatizar_carga_bigquery(
    csv_path=csv_file,
    project_id="r2d-interno-dev",
    dataset_id="raw_okticket",
    table_id="okticket_expenses_raw"
    )

def subir_empresas():
    bucket_name = "prueba-okticket"
    bucket_csv = "bucket-companies"
    empresas_file = f'empresas.csv'
    subir_a_bucket(empresas_file,bucket_name,bucket_csv)

    automatizar_carga_bigquery(
    csv_path=empresas_file,
    project_id="r2d-interno-dev",
    dataset_id="raw_okticket",
    table_id="okticket_companies_raw"
    )

def subir_users():
    bucket_name = "prueba-okticket"
    bucket_csv = "bucket-users"
    empresas_file = f'usuarios.csv'
    subir_a_bucket(empresas_file,bucket_name,bucket_csv)

    automatizar_carga_bigquery(
    csv_path=empresas_file,
    project_id="r2d-interno-dev",
    dataset_id="raw_okticket",
    table_id="okticket_users_raw"
    )


if __name__ == "__main__":
    load_dotenv()
    main()
    subir_expenses()
    subir_empresas()
    subir_users()


