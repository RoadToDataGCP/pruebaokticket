import constantes
import requests as rq
from controlerrores import control_errores
import os

def obtener_tokend():
    url = f'{os.getenv('HOST')}/oauth/token'
    payload = {
        "grant_type": "password",
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "username": os.getenv("OKTICKET_USERNAME"),
        "password": os.getenv("OKTICKET_PASSWORD"),
        "scope": os.getenv("SCOPE")
    }
    files=[]
    headers = {}
    respuesta = rq.post(url,headers=headers, data=payload, files=files)
    datos = control_errores(respuesta)
    constantes.TOKEND = datos['access_token']
    constantes.REFRESHTOKEND = datos['refresh_token']


def refrescar_tokend():
    url = f'{os.getenv('HOST')}/oauth/token'
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": constantes.REFRESHTOKEND,
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "scope": os.getenv("SCOPE")
    }
    files=[]
    headers = {}
    respuesta = rq.post(url,headers=headers, data=payload, files=files)
    datos = control_errores(respuesta)
    constantes.TOKEND = datos['access_token']
    constantes.REFRESHTOKEND = datos['refresh_token']