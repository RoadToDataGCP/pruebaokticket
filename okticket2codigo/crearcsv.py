import pandas as pd

def crear_csv_user(datosuser):
    df = pd.json_normalize(datosuser)
    contenido = pd.json_normalize(df['data'])
    contenidoT = contenido.T.reset_index()
    allcontenido = pd.json_normalize(contenidoT[0]) 
    allcontenido['companies'] = allcontenido['companies'].apply(lambda x: next(iter(x or []), {}).get('id'))
    allcontenido.to_csv("okticket2codigo/csv/users.csv", mode="w", index=False)
    print("CSV users creado")


def crear_csv_reports(datosreports):
    df = pd.json_normalize(datosreports)
    contenido = pd.json_normalize(df['data'])
    contenidoT = contenido.T.reset_index()
    allcontenido = pd.json_normalize(contenidoT[0]) 
    allcontenido.drop('status_log', axis=1, inplace=True)
    allcontenido['expenses'] = allcontenido['expenses'].apply(lambda lista: [g['_id'] for g in lista if isinstance(g, dict) and '_id' in g] if isinstance(lista, list) else [])
    allcontenido.to_csv("okticket2codigo/csv/reports.csv", mode="w", index=False)
    print("CSV reports creado")

        
def crear_csv_basico(datos,nombre):
    df = pd.json_normalize(datos)
    contenido = pd.json_normalize(df['data'])
    contenidoT = contenido.T.reset_index()
    allcontenido = pd.json_normalize(contenidoT[0])
    allcontenido.to_csv(f'okticket2codigo/csv/{nombre}.csv', index=False)
    print(f'CSV {nombre}.csv creado')