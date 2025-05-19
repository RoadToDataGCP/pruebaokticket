from faker import Faker
from obtenertoken import obtenerTokend
from empresa import crearEmpresa, verEmpresas
from users import createUser
from utils import obtenernameid, obtener_ids_users_companies
from expenses import create_gasto
import constantes
def main():
    fake = Faker()

    # Obtener tocken 
    obtenerTokend(408, "8sMHrD2BHBuCjMtEvvNfY8ZqCD8YAjSFh3d8etWZ", "admin@roadtodata.com", "Rtd:2025")

    token = constantes.TOKEND
    #crearEmpresa()
    #Obtener lista de empresas
    empresas = verEmpresas()
    #print(empresas)
    nameid = obtenernameid(empresas)
    for empresa in nameid:
        name = empresa["name"]
        company_id = empresa["id"]
        for _ in range(3):
            print(f"Creando usuario para la empresa {name} con ID {company_id}")
            # Crear usuario
            #createUser(name, fake.name(), fake.email(), fake.password(), [company_id] , "1234", "1234", "1234")

    relaciones = obtener_ids_users_companies(token)

    for relacion in relaciones:
        user_id = relacion["id_user"]
        company_id = relacion["id_company"]
        print(f"Creando gasto para la empresa {name} con ID {company_id} y usuario {user_id}")
        create_gasto(token, company_id, user_id)


if __name__ == "__main__":
    main()