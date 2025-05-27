from faker import Faker
from utils import generar_cif_random, obtener_dict_namecompany_idcompany, obtener_dict_idept_idcompany, obtener_dict_emailusers_idusers, obtener_dict_iduser_idcompany, obtener_dict_iduser_idcompany_idticket
from obtenertoken import obtener_tokend
from company import crear_company, listado_total_company
from users import crear_user, listado_total_users, listado_users_de_una_company, asociar_user_a_department
from departments import crear_deparments, listado_total_deparments
from expenses import crear_expenses, listado_total_expenses
from reports import create_report, listado_total_reports
from crearcsv import crear_csv_user, crear_csv_basico, crear_csv_reports
from subirgooglecloud import subirabucket, creartablaBigQuery
from dotenv import load_dotenv

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
        id_dept = iddept_idcompany["id_dept"]
        id_company = iddept_idcompany["id_company"]

        listauserscompany = listado_users_de_una_company(id_company)
        lista_iduser_idcompany = obtener_dict_emailusers_idusers(listauserscompany)

        userseleccionado = random.choice(lista_iduser_idcompany)
        emailuser = userseleccionado['email']
        iduser = userseleccionado['id']

        print(f"Asociando {emailuser} de la emp {id_company} al dept {id_dept}")
        #asociar_user_a_department(iduser,emailuser,id_company,id_dept)
        #create_report(id_company, id_user, [], f'Hoja de gasto de {id_dept}')
    
    #csv
    crear_csv_basico(datosdepartments, "departments")

# GASTOS
    #crear
    lista_idcompany_iduser = obtener_dict_iduser_idcompany(datosuser)
    for idcompany_iduser in lista_idcompany_iduser:
        id_user = idcompany_iduser["id_user"]
        id_company = idcompany_iduser["id_company"]
        date = fake.date_time_between(start_date='-30d', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
        amount = round(random.uniform(10.00, 500.00), 2)
        name = fake.sentence(nb_words=3).rstrip('.')
        comments = fake.text(max_nb_chars=100)
        print(f"Crear gasto para la la emp {id_company} y el usuario {id_user} con nombre {name}")
        #crear_expenses(id_company, id_user, date, amount, name, comments)

    #csv
    datosexpenses = listado_total_expenses()
    crear_csv_basico(datosexpenses, "expenses")

# HOJA DE GASTOS
    #crear
    lista_idcompany_iduser_idticket = obtener_dict_iduser_idcompany_idticket(datosexpenses)
    for idcompany_iduser_idticket in lista_idcompany_iduser_idticket:
        id_company = idcompany_iduser_idticket["id_company"],
        id_user = idcompany_iduser_idticket["id_user"],
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

"""
    subirabucket('okticket2codigo/csv/company.csv', 'prueba-okticket')
    subirabucket('okticket2codigo/csv/users.csv', 'prueba-okticket')
    subirabucket('okticket2codigo/csv/departsments.csv', 'prueba-okticket')
    subirabucket('okticket2codigo/csv/expenses.csv', 'prueba-okticket')
    subirabucket('okticket2codigo/csv/reports.csv', 'prueba-okticket')

    creartablaBigQuery('okticket2codigo/csv/company.csv', 'raw_okticekt', 'okticket_company_raw')
    creartablaBigQuery('okticket2codigo/csv/users.csv', 'raw_okticekt', 'okticket_users_raw')
    creartablaBigQuery('okticket2codigo/csv/departsments.csv', 'raw_okticekt', 'okticket_departsments_raw')
    creartablaBigQuery('okticket2codigo/csv/expenses.csv', 'raw_okticekt', 'okticket_expenses_raw')
    creartablaBigQuery('okticket2codigo/csv/reports.csv', 'raw_okticekt', 'okticket_reports_raw')
"""

