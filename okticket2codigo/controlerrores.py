def control_errores(respuesta):
    try:
        if respuesta.status_code == 200:
            return respuesta.json()
        elif respuesta.status_code == 201:
            return respuesta.json()
        elif respuesta.status_code == 204:
            print("El ususario se ha borrado con exito")
        # Trata de errores 
        elif respuesta.status_code == 400:
            print("Error 400: petición erronea")
            return respuesta.json()
        elif respuesta.status_code == 401:
            print("Error 401: no tienes autorización")
        elif respuesta.status_code == 403:
            print("Error 403: no tienes permisos")
        elif respuesta.status_code == 404:
            print("Error 404: endpoint erroneo")
        elif respuesta.status_code == 405:
            print("Error 405: método no permitido. Verifica si usas GET o POST correctamente.")
        elif respuesta.status_code == 429:
            print("Error 429: demasidas peticiones")  
        elif respuesta.status_code == 500:
            print("Error 500: en el servidor de la api")
        elif respuesta.status_code == 502:
            print("Error 502: servidor caido") 
        else:
            print("Error: otro error")
        print (respuesta.content)
        return None
    except Exception as e:
        print(f"Error: {e}") 
        print (respuesta.content)
        return None