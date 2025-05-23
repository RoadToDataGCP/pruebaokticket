import requests
import json
import pandas as pd
import constantes
from controlerrores import controlErrores
import os
from faker import Faker
import random
import string

def autUser():
  url = "https://apipre.okticket.es/v2/public/oauth/token"


  payload={'grant_type': 'password',
  'client_id': '408',
  'client_secret': '8sMHrD2BHBuCjMtEvvNfY8ZqCD8YAjSFh3d8etWZ',
  'username': 'admin@roadtodata.com',
  'password': 'Rtd:2025',
  'scope': '*'}
  files=[

  ]
  headers = {}

  response = requests.request("POST", url, headers=headers, data=payload, files=files)

  data = response.json()
  df = pd.json_normalize(data)
  normal = df.loc[0,'access_token']
  return normal


def verEmpresas():
  url = "https://apipre.okticket.es/v2/public/api/companies"

  payload={}
  headers = {
    'Authorization': f'Bearer {autUser()}',
    'Accept': 'application/json'
  }
  
  response = requests.request("GET", url, headers=headers, data=payload)
  current_path = os.path.dirname(os.path.abspath(__file__))
  data = response.json()
  df = pd.json_normalize(data)
  empresas = pd.json_normalize(df["data"])
  empresasT = empresas.T.reset_index()
  allEmpresas = pd.json_normalize(empresasT[0])
  allEmpresas.to_csv(f'{current_path}/empresas.csv', index=False)
  return allEmpresas

print(verEmpresas())

def verEmpresa(id: int):
  url = f"https://apipre.okticket.es/v2/public/api/companies/{id}"

  payload={}
  headers = {
    'Authorization': f'Bearer {autUser()}',
    'Accept': 'application/json'
  }

  response = requests.request("GET", url, headers=headers, data=payload)

  data = response.json()
  df = pd.json_normalize(data)

  return df

#print(verEmpresa(73827))


def verEmpresaCif(cif):
  url = f"https://apipre.okticket.es/v2/public/api/companies?cif={cif}"
  payload={}
  headers = {
    'Authorization': f'Bearer {autUser()}',
    'Accept': 'application/json'
  }

  response = requests.request("GET", url, headers=headers, data=payload)

  data = response.json()
  df = pd.json_normalize(data)
  empresa = pd.json_normalize(df['data'])
  empresa1 = pd.json_normalize(empresa[0])
  empresa1.to_json('empresa.json',index=False)
  return empresa1

#print(verEmpresaCif('E112233445'))

def generarCifRandom():
    first_letter = random.choice("ABCDEFGHJNPQRSUVW")
    digits = ''.join(random.choices(string.digits, k=7))
    control_char = random.choice(string.digits + string.ascii_uppercase)
    cif = f"{first_letter}{digits}{control_char}"
    return cif


def crearEmpresa():
  
  fake = Faker('es_ES')
  url = f'{constantes.HOST}/api/companies'
  for _ in range(5):
    payload=f'cif={generarCifRandom()}&name={fake.company()}&fiscal_address={fake.address()}&postal_code={fake.postal_code()}&city={fake.city()}&contact_number={fake.phone_number()}&contact_email={fake.company_email()}&language=ES'
    headers = {
      'Authorization': f'Bearer {constantes.TOKEND}',
      'Accept': 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    datos = controlErrores(response)

def borrarEmpresa(idemp, nameemp):
  url = f'{constantes.HOST}/api/companies/{idemp}'

  payload = ""
  headers = {
    'Authorization': f'Bearer {constantes.TOKEND}',
    'Accept': 'application/json',
    'company': nameemp
  }

  response = requests.request("DELETE", url, headers=headers, data=payload)

  datos = controlErrores(response)
  return(datos)
      

#crearEmpresa()



departamentos = ['Marketing y Comunicación','Recursos Humanos','Ventas y Desarrollo de Negocio']
conste = autUser()
def crearDepartamento():
  url='https://apipre.okticket.es/v2/public/api/departments'

  for depart in departamentos:
    payload = json.dumps({
      "name": f"{depart}",
      "company_id": 73413
    })
    headers = {
      'Authorization': f'Bearer {conste}',
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

  print('Todo Ok')



#crearDepartamento()


def mostrarDeparts():
  url='https://apipre.okticket.es/v2/public/api/departments'

  payload = json.dumps({

  })
  headers = {
    'Authorization': f'Bearer {autUser()}',
    'Content-Type': 'application/json'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  data  = response.json()
  df = pd.json_normalize(data)
  dfT  = pd.json_normalize(df['data'])
  dfTt = dfT.T.reset_index()
  normalizado = pd.json_normalize(dfTt[0])
  print(normalizado)

mostrarDeparts()