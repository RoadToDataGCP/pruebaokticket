import constantes 
from obtenertoken import obtenerTokend, refrescarTokend
from users import createUser, obtenerListaTotalUsuarios, obtenerMiUsuario

bandera = True

if __name__ == "__main__":
    while(bandera):
        opcion = int(input("Inserte opción: "))
        match opcion:
            case 1: # Ontener tokend
                obtenerTokend(408, "8sMHrD2BHBuCjMtEvvNfY8ZqCD8YAjSFh3d8etWZ", "admin@roadtodata.com", "Rtd:2025")
            case 2: # Refresacar tokend
                refrescarTokend(408, "8sMHrD2BHBuCjMtEvvNfY8ZqCD8YAjSFh3d8etWZ", constantes.REFRESHTOKEND)
            case 3: # Crear usuario
                createUser("JRS-Enterprises", "Javi", "javiii1115.correo@gmail.com", "Hola123456*", [73825] , "1234", "1234", "1234")
                createUser("JRS-Enterprises", "Javi", "javiii1115.correo@gmail.com", "Hola123456*", [73825] , "1234", "1234", "1234")
            case 4: # Lista de usuarios
                obtenerListaTotalUsuarios("JRS-Enterprises")
            case 5: # Mi usuario
                obtenerMiUsuario()
            case _: # Refresacar tokend
                print("Salir")
                bandera = False