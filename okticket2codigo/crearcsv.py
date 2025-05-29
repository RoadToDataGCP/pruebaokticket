import pandas as pd
from utils import calcular_huella_de_carbono
import os


def crear_csv_user(datosuser):
    df = pd.json_normalize(datosuser)
    contenido = pd.json_normalize(df['data'])
    contenidoT = contenido.T.reset_index()
    allcontenido = pd.json_normalize(contenidoT[0]) 
    allcontenido['companies'] = allcontenido['companies'].apply(lambda x: next(iter(x or []), {}).get('id'))
    os.makedirs('okticket2codigo/output', exist_ok=True)
    allcontenido.to_csv("okticket2codigo/output/users.csv", mode="w", index=False)
    print("CSV users creado")


def crear_csv_reports(datosreports):
    df = pd.json_normalize(datosreports)
    contenido = pd.json_normalize(df['data'])
    contenidoT = contenido.T.reset_index()
    allcontenido = pd.json_normalize(contenidoT[0]) 
    allcontenido.drop('status_log', axis=1, inplace=True)
    allcontenido.drop('user', axis=1, inplace=True)
    allcontenido['expenses'] = allcontenido['expenses'].apply(lambda lista: [g['_id'] for g in lista if isinstance(g, dict) and '_id' in g] if isinstance(lista, list) else [])
    os.makedirs('okticket2codigo/output', exist_ok=True)
    allcontenido.to_csv("okticket2codigo/output/reports.csv", mode="w", index=False )
    print("CSV reports creado")


def crear_csv_expenses(datosexpenses):
    df = pd.json_normalize(datosexpenses)
    contenido = pd.json_normalize(df['data'])
    contenidoT = contenido.T.reset_index()
    allcontenido = pd.json_normalize(contenidoT[0])

    allcontenido.rename(columns={'custom_fields.Combustible': 'combustible'}, inplace=True)
    allcontenido.rename(columns={'custom_fields.Litros': 'litros'}, inplace=True)
    allcontenido['huella_de_carbono'] = allcontenido.apply(lambda fila: calcular_huella_de_carbono(fila['combustible'], fila['litros'])if pd.notna(fila.get('combustible')) and pd.notna(fila.get('litros')) else None,axis=1)

    os.makedirs('okticket2codigo/output', exist_ok=True)
    allcontenido.to_csv(f'okticket2codigo/output/expenses.csv', index=False)
    print(f'CSV expenses.csv creado')      


def crear_csv_basico(datos,nombre):
    df = pd.json_normalize(datos)
    contenido = pd.json_normalize(df['data'])
    contenidoT = contenido.T.reset_index()
    allcontenido = pd.json_normalize(contenidoT[0])
    os.makedirs('okticket2codigo/output', exist_ok=True)
    allcontenido.to_csv(f'okticket2codigo/output/{nombre}.csv', index=False)
    print(f'CSV {nombre}.csv creado')