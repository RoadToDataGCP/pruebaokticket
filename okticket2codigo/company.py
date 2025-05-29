import requests
import json
import constantes
from controlerrores import control_errores
import os


def crear_company(cif, name, address, postal_code, city, contact_number, contact_email):
    url = f"{os.getenv('HOST')}/api/companies"
    payload=f'cif={cif}&name={name}&fiscal_address={address}&postal_code={postal_code}&city={city}&contact_number={contact_number}&contact_email={contact_email}&language=ES'
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request('POST', url, headers=headers, data=payload)
    datos = control_errores(response)
    print(json.dumps(datos, indent=4, ensure_ascii=False))

def listado_total_company():
    url = f"{os.getenv('HOST')}/api/companies"

    payload={}
    headers = {
    'Authorization': f'Bearer {constantes.TOKEND}',
    'Accept': 'application/json'
    }

    response = requests.request('GET', url, headers=headers, data=payload)
    datos = control_errores(response)
    return datos

def listado_reports_de_company(idcompany):
    url = f"{os.getenv('HOST')}/api/companies/{idcompany}/reports"
    payload={}
    headers = {
    'Authorization': f'Bearer {constantes.TOKEND}',
    'Accept': 'application/json'
    }

    response = requests.request('GET', url, headers=headers, data=payload)
    datos = control_errores(response)
    return datos