import requests
import json
import pandas as pd
import constantes
from controlerrores import controlErrores
import os
from faker import Faker
import random
import string
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("HOST")
def autUser():
  url = f"{host}/oauth/token"


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
  url = f"{host}/api/companies"

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

#print(verEmpresas())

def verEmpresa(id: int):
  url = f"{host}/api/companies/{id}"

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
  url = f"{host}/api/companies?cif={cif}"
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
  url = f'{host}/api/companies'
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
  url = f'{host}/api/companies/{idemp}'

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
  url=f'{host}/api/departments'

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



#Probando cosas para extraer hojas de gastos y gastos
def mostrarDeparts():
  url=f'{host}/api/departments'

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
  
  return normalizado

#print(mostrarDeparts())


def mostrarGastosDeparts():
  token = autUser()
  headers = {
    'Authorization': f'Bearer {token}'
  }
  expenses = pd.DataFrame()
  departamentos = mostrarDeparts()
  for index,depart in departamentos.iterrows():
    url=f'{host}/api/departments/{depart['id']}/expenses'
    payload={}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    df = pd.json_normalize(data)
    exp = pd.json_normalize(df['data'])
    expenses = pd.concat([expenses,exp],ignore_index=True)

  expenses1=  pd.json_normalize(expenses[0])
  expenses2 = pd.concat([expenses[1]])
  expenses2 = expenses2.dropna()
  expensesTotal = pd.DataFrame()
  expensesTotal = pd.json_normalize(expenses2)
  expensesTotal  = pd.concat([expensesTotal,expenses1], ignore_index=True)
  expensesTotal.to_csv('gastosVarios.csv',index=False)
  
  print(expensesTotal)

#mostrarGastosDeparts()


def mostrarReports():

  url = f"{host}/api/reports"

  payload={}
  headers = {
    'Authorization': f'Bearer {autUser()}',
    'Accept': 'application/json',
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  data = response.json()

  df = pd.json_normalize(data)
  dfN = pd.json_normalize(df['data'])
  dfnT = dfN.T.reset_index()
  normalizdo = pd.json_normalize(dfnT[0])
  print(normalizdo[['id','name','user_id','company_id','department_id','status_id','created_at','updated_at']])


mostrarReports()