from faker import Faker
from obtenertoken import obtenerTokend
from empresa import crearEmpresa, verEmpresas
from users import createUser, obtenerListaTotalUsuarios
from utils import obtenernameid, obtener_ids_users_companies, convertir_json_a_csv_expenses, subir_a_bucket, automatizar_carga_bigquery, crearCsvUsuarios
from expenses import create_gasto
import constantes
from datetime import datetime

def main():

    # Crear una instancia de Faker
    fake = Faker()
    # Obtener tocken 
    obtenerTokend(408, "8sMHrD2BHBuCjMtEvvNfY8ZqCD8YAjSFh3d8etWZ", "admin@roadtodata.com", "Rtd:2025")

    token = constantes.TOKEND
    #crearEmpresa()
    #Obtener lista de empresas
    empresas = verEmpresas()
    #print(empresas)
    nameid = obtenernameid(empresas)
    for empresa in nameid:
        name = empresa["name"]
        company_id = empresa["id"]
        for _ in range(3):
            print(f"Creando usuario para la empresa {name} con ID {company_id}")
            # Crear usuario
            #createUser(name, fake.name(), fake.email(), fake.password(), [company_id] , "1234", "1234", "1234")

    relaciones = obtener_ids_users_companies(token)

    for relacion in relaciones:
        user_id = relacion["id_user"]
        company_id = relacion["id_company"]
        print(f"Creando gasto para la empresa {name} con ID {company_id} y usuario {user_id}")
        create_gasto(token, company_id, user_id)

    datos = obtenerListaTotalUsuarios()
    crearCsvUsuarios(datos)

def subir_expenses():
    #Conversion de json de gastos a csv
    fecha = datetime.now().strftime("%Y%m%d")
    filename = f"expenses_{fecha}.json"
    csv_file = f"expenses_{fecha}.csv"
    convertir_json_a_csv_expenses(filename, csv_file)

    #Subir a bucket
    bucket_name = "prueba-okticket/bucket-gastos"
    subir_a_bucket(f"expenses_{fecha}.csv", bucket_name)
    print(f"Archivo {filename} subido a {bucket_name}.")

    automatizar_carga_bigquery(
    csv_path=csv_file,
    project_id="r2d-interno-dev",
    dataset_id="raw_okticket",
    table_id="okticket_expenses_raw"
    )

if __name__ == "__main__":
    main()
    subir_expenses()
