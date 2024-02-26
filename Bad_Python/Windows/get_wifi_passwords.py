import subprocess
import re
# Se buscan las contraseñas en el CMD haciendo uso de comandos que no requieren correr como administrador. El script soporta únicamente lenguages en español e inglés.

def get_wifi_passwords():
    try:
        # Utilizando CMD, corremos proceso para obtener todas las redes registradas en el dispositivo.
        profiles_data = subprocess.check_output('netsh wlan show profiles', shell=True, text=True)
    except subprocess.CalledProcessError:
        print("Error al ejecutar el comando.")
        return False
    # Verificamos si recibimos algo de información.
    if not profiles_data:
        print("No se encontraron redes")
        return False
    # Buscamos todos los perfiles con expresión regular. 
    profiles = re.findall(r"All User Profile\s*:\s*(.*)", profiles_data)
    
    # No sabemos si el CMD esta en español o en inglés.
    spanish = False
    spanishLATAM = False
    # Si no se encuentran perfiles en inglés, intentar con la expresión regular en español
    if not profiles:
        print("CMD no esta in inglés, intentando en español.")
        profiles = re.findall(r"Todos los perfiles de usuario\s*:\s*(.*)", profiles_data)
        spanish = True
    else:
        print("Perfiles encontrados, CMD en inglés")

    if spanish and not profiles:
        spanish = False
        print("CMD no esta in español, intentando en español LATAM")
        profiles = re.findall(r"Perfil de todos los usuarios\s*:\s*(.*)", profiles_data)
        spanishLATAM = True
    # Guardaremos en un diccionario todas las claves (Con su red respectiva.)
    wifi_passwords = {}

    for profile in profiles:
        # Obtener la clave de cada perfil dependiendo del idioma
        password_info = subprocess.check_output(f'netsh wlan show profile name="{profile}" key=clear', shell=True, text=True)
        if spanish or spanishLATAM:
            password = re.search(r"Contenido de la clave\s*:\s*(.*)", password_info)
        else:
            password = re.search(r"Key Content\s*:\s*(.*)", password_info)
        
        if password is None:
            wifi_passwords[profile] = None
        else:
            wifi_passwords[profile] = password.group(1)

    return wifi_passwords
print("inicio")
# Ejecutar la función y imprimir los resultados
wifi_passwords = get_wifi_passwords()
print("La función ha corrido")
if wifi_passwords:
    for profile, password in wifi_passwords.items():
        print(f'Perfil: {profile}, Contraseña: {password}')
else:
    print("¿No se encontraron passwords?")