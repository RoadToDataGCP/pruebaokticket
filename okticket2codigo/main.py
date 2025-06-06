from faker import Faker
from utils import generar_cif_random, generar_tipo_combustible, obtener_dict_namecompany_idcompany, obtener_dict_idept_idcompany, obtener_dict_emailusers_idusers, obtener_dict_iduser_idcompany, obtener_dict_iduser_idcompany_idticket, calcular_huella_de_carbono, obtener_dict_iuser_idept_idcompany
from obtenertoken import obtener_tokend
from company import crear_company, listado_total_company
from users import crear_user, listado_total_users, listado_users_de_una_company, asociar_user_a_department, listado_total_users_company_departments
from departments import crear_deparments, listado_total_deparments
from expenses import crear_expenses, listado_total_expenses
from reports import create_report, listado_total_reports
from crearcsv import crear_csv_basico, crear_csv_user, crear_csv_reports, crear_csv_expenses
from subirgooglecloud import subirabucket, creartablaBigQuery
from dotenv import load_dotenv
from datetime import datetime
import random 

def main():
    
    # Crear una instancia de Faker
    fake = Faker('es_ES')

    # Obtener tocken 
    obtener_tokend()

# COMPANY
    #crear
    for _ in range(3):
        name = fake.company()
        print(f"Creando empresa {name}")
        #crear_company(generar_cif_random(), name, fake.address(), fake.postal_code(), fake.city(), fake.phone_number(), fake.company_email())
    
    #csv
    datoscompany = listado_total_company()
    crear_csv_basico(datoscompany, "company")

# USERS
    #crear
    lista_namecompany_idcompany = obtener_dict_namecompany_idcompany(datoscompany)
    for namecompany_idcompany in lista_namecompany_idcompany:
        name = namecompany_idcompany["name"]
        company_id = namecompany_idcompany["id"]
        for _ in range(random.randint(2,5)):
            print(f"Creando usuario para la empresa {name} con ID {company_id}")
            #crear_user(fake.name(), fake.email(), fake.password(), [company_id] , "1234", "1234", "1234")
    
    #csv
    datosuser = listado_total_users()
    crear_csv_user(datosuser)
    
# DEPARTMENTS
    #crear 
    lista_namecompany_idcompany = obtener_dict_namecompany_idcompany(datoscompany)
    departments = ['Marketing y Comunicación','Recursos Humanos','Ventas y Desarrollo de Negocio']
    for namecompany_idcompany in lista_namecompany_idcompany:
        name = namecompany_idcompany["name"]
        company_id = namecompany_idcompany["id"]
        for namedept in departments:
            print(f"Creando departamento {namedept} para la empresa {name} con ID {company_id}")
            #crear_deparments(namedept, company_id)

    #asociar user a un dept 
    datosdepartments = listado_total_deparments()
    lista_iddept_idcompany = obtener_dict_idept_idcompany(datosdepartments)
    for iddept_idcompany in lista_iddept_idcompany:
        id_department = iddept_idcompany["id_dept"]
        id_company = iddept_idcompany["id_company"]

        listauserscompany = listado_users_de_una_company(id_company)
        lista_iduser_idcompany = obtener_dict_emailusers_idusers(listauserscompany)

        userseleccionado = random.choice(lista_iduser_idcompany)
        email_user = userseleccionado['email']
        iduser = userseleccionado['id']
        print(f"Asociando {email_user} de la emp {id_company} al dept {id_department}")
        #asociar_user_a_department(iduser,emailuser,id_company,id_dept)
                
    #csv
    datosdepartments = listado_total_deparments()
    crear_csv_basico(datosdepartments, "departments")

# GASTOS
#EL ID DE DEPARTAMENTO ME LO INVENTO 
    #crear
    lista_idcompany_iduser = obtener_dict_iduser_idcompany(datosuser)
    lista_idcompany_iduser = random.choices(lista_idcompany_iduser,k=random.choice(range(2,5)))
    for idcompany_iduser in lista_idcompany_iduser:
        id_user = idcompany_iduser["id_user"]
        id_company = idcompany_iduser["id_company"]
        date = datetime.now().strftime('%Y-%m-%dT%H:%M')
        amount = round(random.uniform(10.00, 500.00), 2)
        name = fake.sentence(nb_words=3).rstrip('.')
        comments = fake.text(max_nb_chars=100)
        combustible = generar_tipo_combustible()
        litros = fake.random_int(100,300)
        print(f"Crear gasto para la la emp {id_company} y el usuario {id_user} con nombre {name}")
        #crear_expenses(id_company, id_user, date, amount, name, comments, combustible, litros)

    #csv
    datosexpenses = listado_total_expenses()
    crear_csv_expenses(datosexpenses)

# HOJA DE GASTOS
    #crear
    lista_idcompany_iduser_idticket = obtener_dict_iduser_idcompany_idticket(datosexpenses)
    for idcompany_iduser_idticket in lista_idcompany_iduser_idticket:
        id_company = idcompany_iduser_idticket["id_company"]
        id_user = idcompany_iduser_idticket["id_user"]
        ids_ticket = idcompany_iduser_idticket["ids_ticket"]
        name = fake.sentence(nb_words=3).rstrip('.')
        print(f"Crear hoja de gasto para la la emp {id_company} y el usuario {id_user}")
        #create_report(id_company, id_user, ids_ticket, name)
    
    #csv
    datosreports = listado_total_reports()
    crear_csv_reports(datosreports)

if __name__ == "__main__":
    load_dotenv()
    main()
    
    subirabucket('okticket2codigo/output/company.csv', 'prueba-okticket')
    subirabucket('okticket2codigo/output/users.csv', 'prueba-okticket')
    subirabucket('okticket2codigo/output/departments.csv', 'prueba-okticket')
    subirabucket('okticket2codigo/output/expenses.csv', 'prueba-okticket')
    subirabucket('okticket2codigo/output/reports.csv', 'prueba-okticket')


    creartablaBigQuery('okticket2codigo/output/company.csv', 'raw_okticket', 'okticket_company_raw')
    creartablaBigQuery('okticket2codigo/output/users.csv', 'raw_okticket', 'okticket_users_raw')
    creartablaBigQuery('okticket2codigo/output/departments.csv', 'raw_okticket', 'okticket_departsments_raw')
    creartablaBigQuery('okticket2codigo/output/expenses.csv', 'raw_okticket', 'okticket_expenses_raw')
    creartablaBigQuery('okticket2codigo/output/reports.csv', 'raw_okticket', 'okticket_reports_raw')

