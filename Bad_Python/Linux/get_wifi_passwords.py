#################
# NOTA1: Este código no ha sido probado, meramente teórico. 
# NOTA2: Este script solo funciona en dispositivos linux que tengan instalado Network Manager.
## sudo apt update
## sudo apt-get install network-manager
## nmcli --version #Para confirmar que esta instalado.



import subprocess

def get_wifi_passwords():
    try:
        # Obtener los nombres de las redes Wi-Fi guardadas
        saved_networks = subprocess.check_output("nmcli -t -f NAME con show", shell=True, text=True).splitlines()

        wifi_passwords = {}

        for network in saved_networks:
            try:
                # Obtener la contraseña de cada red guardada
                password_cmd = f"nmcli -s -g 802-11-wireless-security.psk connection show '{network}'"
                password = subprocess.check_output(password_cmd, shell=True, text=True).strip()
                wifi_passwords[network] = password
            except subprocess.CalledProcessError:
                wifi_passwords[network] = None

        return wifi_passwords

    except subprocess.CalledProcessError:
        print("Error al ejecutar el comando nmcli.")
        return False

# Ejecutar la función y imprimir los resultados
wifi_passwords = get_wifi_passwords()
if wifi_passwords:
    for network, password in wifi_passwords.items():
        print(f'Red: {network}, Contraseña: {password}')

