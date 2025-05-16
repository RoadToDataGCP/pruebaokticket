from faker import Faker
from obtenertoken import obtenerTokend
from empresa import crearEmpresa, verEmpresas
from users import createUser
from utils import obtenernameid

fake = Faker()

# Obtener tocken 
obtenerTokend(408, "8sMHrD2BHBuCjMtEvvNfY8ZqCD8YAjSFh3d8etWZ", "admin@roadtodata.com", "Rtd:2025")

#crearEmpresa()
# Obtener lista de empresas
empresas = verEmpresas()
nameid = obtenernameid(empresas)
for empresa in nameid:
    name = empresa["name"]
    id = empresa["id"]
    for _ in range(3):
        createUser(name, fake.name(), fake.email(), fake.password(), [id] , "1234", "1234", "1234")