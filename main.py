from faker import Faker
from obtenertoken import obtenerTokend
from empresa import crearEmpresa, verEmpresas, crearDepartamento, mostrarDeparts
from users import createUser, obtenerListaTotalUsuarios, asociar_usuario_a_dept, listado_email_users_de_empresa
from utils import obtener_nameid, obtener_ids_users_companies, convertir_json_a_csv_expenses, subir_a_bucket, automatizar_carga_bigquery, crearCsvUsuarios, obtener_deptid_empid
from expenses import create_gasto
import constantes
from datetime import datetime
import random

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
    listacompany = list()
    nameid = obtener_nameid(empresas)
    for empresa in nameid:
        name = empresa["name"]
        company_id = empresa["id"]
        listacompany.append(company_id)
        for _ in range(3):
            print(f"Creando usuario para la empresa {name} con ID {company_id}")
            # Crear usuario
            #createUser(name, fake.name(), fake.email(), fake.password(), [company_id] , "1234", "1234", "1234")
    """
    relaciones = obtener_ids_users_companies(token)

    for relacion in relaciones:
        user_id = relacion["id_user"]
        company_id = relacion["id_company"]
        print(f"Creando gasto para la empresa {name} con ID {company_id} y usuario {user_id}")
        #create_gasto(token, company_id, user_id)
    """
    datos = obtenerListaTotalUsuarios()
    crearCsvUsuarios(datos)

    #Crear dept
    #crearDepartamento()

    #Obtener id de los departamentos
    dept = mostrarDeparts()
    deptidcompanyid = obtener_deptid_empid(dept)

    for dept in deptidcompanyid:
        id_dept = dept["id_dept"]
        id_company = dept["id_emp"]
        dictusers = listado_email_users_de_empresa(id_company)
        userseleccionado = random.choice(dictusers)
        emailuser = userseleccionado['email']
        iduser = userseleccionado['id']
        print(f"Asociando {emailuser} de la emp {id_company} al dept {id_dept}")
        asociar_usuario_a_dept(iduser,emailuser,id_company,id_dept)


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
    main()
    #subir_expenses()
    #subir_empresas()
    #subir_users()


