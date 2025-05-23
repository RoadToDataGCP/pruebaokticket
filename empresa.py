import requests
import json
import pandas as pd
import constantes
from controlerrores import control_errores
import os

def ver_empresas():
  url = f'{os.getenv('HOST')}/api/companies'

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
  return allEmpresas


def crear_empresa():
  empresas = pd.read_json("empresas.json")
  url = f'{os.getenv('HOST')}/api/companies'
  for empresa in empresas.values:
  
    payload=f'cif={empresa[0]}&name={empresa[1]}&fiscal_address={empresa[2]}&postal_code={empresa[3]}&city={empresa[4]}&contact_number={empresa[5]}&contact_email={empresa[6]}&language={empresa[7]}'
    headers = {
      'Authorization': f'Bearer {constantes.TOKEND}',
      'Accept': 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    datos = control_errores(response)
    print(datos)

#NO SE UTILIZA
def ver_empresa_por_id(id: int):
  url = f'{os.getenv('HOST')}/api/companies/{id}'

  payload={}
  headers = {
    'Authorization':f'Bearer {constantes.TOKEND}',
    'Accept': 'application/json'
  }

  response = requests.request("GET", url, headers=headers, data=payload)

  data = control_errores(response)
  df = pd.json_normalize(data)

  return df


#NO SE UTILIZA
def ver_empresa_por_cif(cif):
  url = f'{os.getenv('HOST')}/api/companies?cif={cif}'
  payload={}
  headers = {
    'Authorization': f'Bearer {constantes.TOKEND}',
    'Accept': 'application/json'
  }

  response = requests.request("GET", url, headers=headers, data=payload)

  data = control_errores(response)

  df = pd.json_normalize(data)
  empresa = pd.json_normalize(df['data'])
  empresa1 = pd.json_normalize(empresa[0])
  empresa1.to_json('empresa.json',index=False)
  return empresa1
  

def borrar_empresa(idemp, nameemp):
  url = f'{os.getenv('HOST')}/api/companies/{idemp}'

  payload = ""
  headers = {
    'Authorization': f'Bearer {constantes.TOKEND}',
    'Accept': 'application/json',
    'company': nameemp
  }

  response = requests.request("DELETE", url, headers=headers, data=payload)

  datos = control_errores(response)
  return(datos)
      