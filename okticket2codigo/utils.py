import random
import string

def generar_cif_random():
    first_letter = random.choice('ABCDEFGHJNPQRSUVW')
    digits = ''.join(random.choices(string.digits, k=7))
    control_char = random.choice(string.digits + string.ascii_uppercase)
    cif = f'{first_letter}{digits}{control_char}'
    return cif

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