from login import login 
import getters
from time import time
from utils import espera_con_barra, formato_hms

def main():

    while True:
        print("\n📋 ¿Qué acción deseas realizar?")
        print("1️⃣  Login")
        print("2️⃣  Cargar datos de empresas")
        print("3️⃣  Cargar datos de usuarios por empresa")
        print("4️⃣  Cargar datos de empresas para clientes")
        print("5️⃣  cargar datos de usuarios por empresa (resumen)")
        print("6️⃣  Proceso completo")
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
            if 'token' not in locals():
                print("❌ Debes iniciar sesión primero.")
                continue
            print("🔄 Cargando datos de empresas...")
            getters.get_companies(token)
        elif opcion == "3":
            empresa = input("👉 Ingresa el ID de la empresa: ").strip()
            getters.get_users(token, empresa)
        elif opcion == "4":
            print("🔄 Cargando datos de empresas para clientes...")
            getters.get_companies_filtered(token)
        elif opcion == "5":
            empresa = input("👉 Ingresa el ID de la empresa: ").strip()
            print("🔄 Cargando datos de usuarios por empresa (resumen)...")
            getters.get_users_companies_summary(token, empresa)
        elif opcion == "6":
            hora_inicio = time.time()
            print("🔄 Iniciando proceso completo...")
            print()
            carga_estaciones=time.time()
            print()
            carga_municipios=time.time()
            print()
            carga_historico=time.time()
            print()
            carga_predicciones=time.time()
            print()
            hora_fin = time.time()
            print("🔄 Proceso completo")
            duracion_estaciones = carga_estaciones - hora_inicio
            duracion_municipios = carga_municipios - carga_estaciones
            duracion_historico = carga_historico - carga_municipios
            duracion_predicciones = carga_predicciones - carga_historico
            duracion_combinacion = hora_fin - carga_predicciones
            print(f"⏱️ Carga de estaciones: {formato_hms(duracion_estaciones)}")
            print(f"⏱️ Carga de municipios: {formato_hms(duracion_municipios)}")
            print(f"⏱️ Carga de histórico: {formato_hms(duracion_historico)}")
            print(f"⏱️ Carga de predicciones: {formato_hms(duracion_predicciones)}")
            print(f"⏱️ Combinación de datos: {formato_hms(duracion_combinacion)}")
            duracion = hora_fin - hora_inicio
            print(f"⏱️ Duración total del proceso: {formato_hms(duracion)}")
        elif opcion == "7":
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