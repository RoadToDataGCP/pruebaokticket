import requests
import json
import constantes
from controlerrores import control_errores
import os
from datetime import datetime


def create_report(id_company, id_user, ticket_id, name):
    url = f'{os.getenv('HOST')}/api/reports'
    headers = {
        'Authorization': f'Bearer {constantes.TOKEND}',
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'name': name,
        'user_id': str(id_user),
        'company_id': id_company,
        'status_id': '0',
        'tickets[]': ticket_id
    }
 
    response = requests.post(url, headers=headers, data=data)
    datos = control_errores(response)
    #print(json.dumps(datos, indent=4, ensure_ascii=False))
    
    
def listado_total_reports():
    date = datetime.now().strftime('%Y-%m-%d')
    url = f'{os.getenv('HOST')}/api/reports?with=user,expenses&updated_date_min=1999-01-01T01:01&updated_date_max={date}T23:59'
    payload={}
    headers = {
    'Authorization': f'Bearer {constantes.TOKEND}',
    'Accept': 'application/json'
    }

    response = requests.request('GET', url, headers=headers, data=payload)
    datos = control_errores(response)
    return datos