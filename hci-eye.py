import bluetooth
import json
import time
from datetime import datetime

# Nome do arquivo onde os dados serão salvos
output_file = 'bluetooth_devices.json'

# Função para carregar dispositivos do arquivo
def load_devices():
    try:
        with open(output_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Função para salvar dispositivos no arquivo
def save_devices(devices):
    with open(output_file, 'w') as file:
        json.dump(devices, file, indent=4)

# Função para escanear dispositivos Bluetooth
def scan_bluetooth_devices():
    print("Escaneando dispositivos Bluetooth...")
    discovered_devices = bluetooth.discover_devices(lookup_names=True)
    
    devices = load_devices()
    
    for addr, name in discovered_devices:
        if addr not in devices:
            devices[addr] = {
                'name': name,
                'first_found': str(datetime.now()),
                'last_found': str(datetime.now())
            }
        else:
            devices[addr]['last_found'] = str(datetime.now())
    
    save_devices(devices)
    print(f"Encontrados {len(discovered_devices)} dispositivos.")

if __name__ == "__main__":
    try:
        while True:
            scan_bluetooth_devices()
            time.sleep(10)  # Espera 10 segundos antes da próxima varredura
    except KeyboardInterrupt:
        print("\nEscaneamento interrompido.")