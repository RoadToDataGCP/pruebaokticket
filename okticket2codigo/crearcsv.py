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
    allcontenido['expenses'] = allcontenido['expenses'].apply(lambda lista: [g['_id'] for g in lista if isinstance(g, dict) and '_id' in g] if isinstance(lista, list) else [])
    os.makedirs('okticket2codigo/output', exist_ok=True)
    allcontenido.to_csv("okticket2codigo/output/reports.csv", mode="w", index=False )
    print("CSV reports creado")


def crear_csv_expenses(datosexpenses):
    df = pd.json_normalize(datosexpenses)
    contenido = pd.json_normalize(df['data'])
    contenidoT = contenido.T.reset_index()
    allcontenido = pd.json_normalize(contenidoT[0])

    allcontenido['combustible'] = None
    allcontenido['litros'] = None
    allcontenido['huella_de_carbono'] = None

    if 'custom_fields' in df.columns:
        custom_fields_df = pd.json_normalize(df['custom_fields'].apply(lambda x: x if isinstance(x, dict) else {}))
        if 'combustible' in custom_fields_df.columns:
            allcontenido['combustible'] = custom_fields_df['combustible']
        if 'litros' in custom_fields_df.columns:
            allcontenido['litros'] = custom_fields_df['litros']
        if  allcontenido['combustible'].notna() & allcontenido['litros'].notna():
            allcontenido['huella_de_carbono'].apply(calcular_huella_de_carbono(allcontenido.loc('combustible'), allcontenido.loc('litros')))

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