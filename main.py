from faker import Faker
from obtenertoken import obtenerTokend
from empresa import crearEmpresa, verEmpresas, borrarEmpresa
from users import createUser, obtenerListaTotalEmpresas, obtenerListaTotalUsuarios, borrarUsuario
from utils import obtenernameid, obtenernameid2, obteneruseridempresaid
import json

fake = Faker()

# Obtener tocken 
obtenerTokend(408, "8sMHrD2BHBuCjMtEvvNfY8ZqCD8YAjSFh3d8etWZ", "admin@roadtodata.com", "Rtd:2025")

#crearEmpresa()
# Obtener lista de empresas

empresas = verEmpresas()
nameid = obtenernameid(empresas)
"""
for empresa in nameid:
    name = empresa["name"]
    id = empresa["id"]
    for _ in range(3):
        createUser(name, fake.name(), fake.email(), fake.password(), [id] , "1234", "1234", "1234")

for empresa in nameid:
    name = empresa["name"]
    id = empresa["id"]
    borrarEmpresa(id, name)
      


empresas = obtenerListaTotalEmpresas()
nameid = obtenernameid2(empresas)

#print(json.dumps(nameid, indent=2))

usuarios = obtenerListaTotalUsuarios()
useridempid = obteneruseridempresaid(usuarios)
print(json.dumps(useridempid, indent=2))
""" 

borrarUsuario(198273)