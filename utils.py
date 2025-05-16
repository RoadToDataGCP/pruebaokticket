import random
import time
import threading
from tqdm import tqdm

def obtenernameid(empresas):
    nombreid = list()
    for _, empresa in empresas.iterrows():
        nombreid1 = {
            'name': empresa["name"],
            'id': empresa["id"]
        }
        nombreid.append(nombreid1)
    return nombreid



def espera_con_barra(segundos: int, mensaje: str = "Esperando"):
    hilo = threading.current_thread().name
    for _ in tqdm(range(segundos), desc=f"⏳ {mensaje} - {hilo}", ncols=150):
        time.sleep(1)

def formato_hms(segundos):
    return time.strftime("%H:%M:%S", time.gmtime(segundos))
