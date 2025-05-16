import constantes
import requests as rq
from controlerrores import controlErrores

def obtenerTokend(client_id, client_secret, username, password):
    url = f'{constantes.HOST}/oauth/token'
    payload = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password,
        "scope": "*"
    }
    files=[]
    headers = {}
    respuesta = rq.post(url,headers=headers, data=payload, files=files)
    datos = controlErrores(respuesta)
    constantes.TOKEND = datos['access_token']
    constantes.REFRESHTOKEND = datos['refresh_token']

def refrescarTokend(client_id, client_secret, refreshtokend):
    url = f'{constantes.HOST}/oauth/token'
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refreshtokend,
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "*"
    }
    files=[]
    headers = {}
    respuesta = rq.post(url,headers=headers, data=payload, files=files)
    datos = controlErrores(respuesta)
    constantes.TOKEND = datos['access_token']
    constantes.REFRESHTOKEND = datos['refresh_token']
   

