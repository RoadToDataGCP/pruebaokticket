import random
import string
import pandas as pd

def generar_cif_random():
    first_letter = random.choice('ABCDEFGHJNPQRSUVW')
    digits = ''.join(random.choices(string.digits, k=7))
    control_char = random.choice(string.digits + string.ascii_uppercase)
    cif = f'{first_letter}{digits}{control_char}'
    return cif


def generar_tipo_combustible():
    df = pd.read_csv('csv/emisiones.csv')
    lista_conbustible = df['Combustible'].tolist()
    return random.choice(lista_conbustible)


def obtener_dict_namecompany_idcompany(datoscompany):
    listacompany = list()
    companies= datoscompany['data']
    for company in companies:
        name_id_company = {
            'name': company["name"],
            'id': company["id"]
        }
        listacompany.append(name_id_company)
    return listacompany


def obtener_dict_emailusers_idusers(datosuser):
    listausers = list()
    users= datosuser['data']
    for user in users:
        email_id_user={
        'email': user['email'],
        'id' : user['id']
        }
        listausers.append(email_id_user)
    return listausers


def obtener_dict_idept_idcompany(datosdepartment):
    listaiddeptidcompany = list()
    departments = datosdepartment['data']
    for department in departments:
        id_department_id_company = {
            'id_dept': department["id"],
            'id_company': department["company_id"]
        }
        listaiddeptidcompany.append(id_department_id_company)
    return listaiddeptidcompany


def obtener_dict_iduser_idcompany(datossuser):
    listaiduseridcompany = list()
    users = datossuser['data']
    for user in users:
        userid= user['id']
        listacompany =  user['companies']
        for company in listacompany:
            id_department_id_company = {
                'id_user': userid,
                'id_company': company["id"]
                }
        listaiduseridcompany.append(id_department_id_company)
    return listaiduseridcompany

def obtener_dict_iuser_idept_idcompany(datossuser):
    listaiduseriddeptidcompany = list()
    users = datossuser['data']
    for user in users:
        userid= user['id']
        useremail= user['email']
        listadepartments =  user['departments']
        for dept in listadepartments:
            id_user_id_department_id_company = {
                'id_user': userid,
                'email_user': useremail,
                'id_department': dept["id"],
                'id_company': dept["company_id"]
                }
        listaiduseriddeptidcompany.append(id_user_id_department_id_company)
    return listaiduseriddeptidcompany



def obtener_dict_iduser_idcompany_idticket(datosexpenses):
    listaiduseridcompanyidticket = list()
    expenses = datosexpenses['data']
    for expens in expenses:
        id_company = expens["company_id"]
        id_user = expens["user_id"]
        id_ticket = expens["_id"]
        
        encontrado = False
        for iduseridcompanyidticket in listaiduseridcompanyidticket:
            if id_company==iduseridcompanyidticket["id_company"] and id_user==iduseridcompanyidticket["id_user"]:
                iduseridcompanyidticket["ids_ticket"].append(id_ticket)
                encontrado = True
                break
        if not encontrado:
            id_user_id_company_id_ticket = {
                'id_company': expens["company_id"],
                'id_user': expens["user_id"],
                'ids_ticket': [expens["_id"]]
            }
            listaiduseridcompanyidticket.append(id_user_id_company_id_ticket)
    return listaiduseridcompanyidticket


def calcular_huella_de_carbono(combustible, litros):
    df_emisiones = pd.read_csv('okticket2codigo/csv/emisiones.csv')
    for _,emisiones in df_emisiones.iterrows():
        if emisiones['Combustible'] == combustible:
            consumo = emisiones['CO2e_kg_por_litro'] 
            return consumo * litros
