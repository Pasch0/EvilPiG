import json
import os

# Caminhos dos arquivos
cracked_file_path = 'wifite3/cracked.txt'
wpa_supplicant_file_path = '/etc/wpa_supplicant/wpa_supplicant-attack.conf'

# Função para ler o arquivo cracked.txt
def read_cracked_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Erro ao ler o arquivo {file_path}: {e}")
        return []

# Função para ler o arquivo wpa_supplicant-attack.conf
def read_wpa_supplicant(file_path):
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r') as file:
        content = file.readlines()
    
    # Extrair redes existentes
    networks = []
    current_ssid = None

    for line in content:
        line = line.strip()
        if line.startswith('ssid='):
            if '=' in line:
                current_ssid = line.split('=')[1].strip().strip('"')
                networks.append(current_ssid)
        elif line.startswith('network={'):
            current_ssid = None  # Reset for the next network block

    return networks

# Função para adicionar uma nova rede ao arquivo wpa_supplicant-attack.conf
def add_network_to_wpa_supplicant(file_path, ssid, psk):
    new_network = f'\nnetwork={{\n    ssid="{ssid}"\n    psk="{psk}"\n    priority=3\n}}\n'
    
    with open(file_path, 'a') as file:
        file.write(new_network)

# Função principal
def main():
    cracked_data = read_cracked_file(cracked_file_path)
    existing_networks = read_wpa_supplicant(wpa_supplicant_file_path)

    for entry in cracked_data:
        ssid = entry.get('essid') or entry.get('ssid')
        psk = entry.get('psk') or entry.get('key')

        if ssid and ssid not in existing_networks:
            print(f"Adicionando rede: {ssid} com senha: {psk}")
            add_network_to_wpa_supplicant(wpa_supplicant_file_path, ssid, psk)
        else:
            if not ssid:
                print("Rede com nome vazio não será adicionada.")
            else:
                print(f"Rede {ssid} já existe no arquivo ou é inválida.")

if __name__ == "__main__":
    main()