import requests
import json
import pandas as pd
import constantes
from controlerrores import controlErrores
import os

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
    'Authorization': f'Bearer {constantes.TOKEND}',
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
  return allEmpresas[['id','name','cif','fiscal_address','postal_code','city','contact_number','contact_email']]

#verEmpresas()

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

def crearEmpresa():
  
  empresas = pd.read_json("empresas.json")
  url = f'{constantes.HOST}/api/companies'
  for empresa in empresas.values:
  
    payload=f'cif={empresa[0]}&name={empresa[1]}&fiscal_address={empresa[2]}&postal_code={empresa[3]}&city={empresa[4]}&contact_number={empresa[5]}&contact_email={empresa[6]}&language={empresa[7]}'
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