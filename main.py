from login import login 
import getters
from time import time
from utils import espera_con_barra, formato_hms
import expenses

def main():
    
    token = login()
    print("✅ Login exitoso.")
    while True:
        print("\n📋 ¿Qué acción deseas realizar?")
        print("1️⃣  Login")
        print("2️⃣  Cargar datos de empresas")
        print("3️⃣  Cargar datos de usuarios por empresa")
        print("4️⃣  Cargar datos de empresas para clientes")
        print("5️⃣  cargar datos de usuarios por empresa (resumen)")
        print("6️⃣  Cargar gastos por empresa")
        print("7️⃣  Limpiar archivos generados")
        print("0️⃣  Salir")

        opcion = input("👉 Ingresa una opción: ").strip()

        if opcion == "1":
            token = login()
            if token:
                print("✅ Login exitoso.")
            else:
                print("❌ Error en el login.")
        elif opcion == "2":
            if token:
                print("🔄 Cargando datos de empresas...")
                getters.get_companies(token)
            else:
                print("❌ Debes iniciar sesión primero.")
        elif opcion == "3":
            if token:
                empresa = input("👉 Ingresa el ID de la empresa: ").strip()
                getters.get_users(token, empresa)
            else:
                print("❌ Debes iniciar sesión primero.")
        elif opcion == "4":
            if token:
                print("🔄 Cargando datos de empresas para clientes...")
                getters.get_companies_filtered(token)
            else:
                print("❌ Debes iniciar sesión primero.")
        elif opcion == "5":
            if token:
                empresa = input("👉 Ingresa el ID de la empresa: ").strip()
                print("🔄 Cargando datos de usuarios por empresa (resumen)...")
                getters.get_users_companies_summary(token, empresa)
            else:
                print("❌ Debes iniciar sesión primero.")
        elif opcion == "6":
            if token:
                empresa = input("👉 Ingresa el ID de la empresa: ").strip()
                print("🔄 Cargando gastos por empresa...")
                getters.get_gastos_by_empresa(token, empresa)
            else:
                print("❌ Debes iniciar sesión primero.")
        elif opcion == "7":
            print("🔄 Creando gastos...")
            empresa = input("👉 Ingresa el ID de la empresa: ").strip()
            expenses.create_gasto(token)
            print("🔄 Mostrando gastos por empresa...")
            expenses.get_gastos_by_empresa(token, empresa)
            print("✅ Archivos generados eliminados.")
        elif opcion == "0":
            print("👋 Saliendo del programa.")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")
    # Call the login function
    #token = login()
    print("Login function executed successfully.")
    #print("Access Token:", token)
    # Add any other main functionality here
    #getters.get_users(token)

if __name__ == "__main__":
    main()