import subprocess
import os
import sys
import json
import time

def crack_handshake(handshake_file, bssid, wordlist):
    try:
        # Comando para quebrar a senha usando aircrack-ng
        command = f"aircrack-ng -w {wordlist} -b {bssid} /opt/EvilPiG/wifite3/hs/{handshake_file}"
        
        # Executa o comando e captura a saída
        process = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Verifica se o comando foi bem-sucedido
        if process.returncode == 0:
            # A saída pode conter a senha crackeada
            output_lines = process.stdout.splitlines()
            
            # Procura pela linha que contém "KEY FOUND!"
            key_found_index = None
            for i, line in enumerate(output_lines):
                if "KEY FOUND!" in line:
                    key_found_index = i
                    break

            if key_found_index is not None:
                # A senha está na mesma linha que "KEY FOUND!"
                password = output_lines[key_found_index + 1].strip().split('KEY FOUND! [')[1].strip()
                # remover [] do inicio e final da senha
                password = password[0:-1].strip().rstrip().lstrip()
                print(f"Senha encontrada: {password}")

                # Cria um novo dicionário para a entrada
                cracked_entry = {
                    "type": "WPS",  # ou outro tipo conforme necessário
                    "date": int(time.time()),  # Usando timestamp atual como exemplo
                    "essid": handshake_file.split('_')[1],  # Extrai o ESSID do nome do arquivo
                    "bssid": bssid.replace('-', ':'),
                    "psk": password  # A senha encontrada
                }

                # Salva a nova entrada no arquivo cracked.txt sem remover as existentes
                save_to_cracked_file(cracked_entry)

                return True
            else:
                print("Não foi possível encontrar a senha na saída.")
                return False
        else:
            print(f"Falha ao quebrar handshake: {handshake_file}. Erro: {process.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"Erro ao executar aircrack-ng: {e}")
        return False

def save_to_cracked_file(new_entry):
    cracked_file_path = "/opt/EvilPiG/wifite3/cracked.txt"

    # Tenta ler o arquivo existente e carregar como JSON
    try:
        with open(cracked_file_path, 'r') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []  # Se o arquivo não existir ou estiver vazio/errado

    # Verifica se a entrada já existe para evitar duplicatas
    for entry in existing_data:
        if entry['bssid'] == new_entry['bssid'] and entry['psk'] == new_entry['psk']:
            print("A senha já está registrada. Não será adicionada novamente.")
            return

    # Adiciona a nova entrada à lista existente
    existing_data.append(new_entry)

    # Salva novamente o JSON no arquivo
    with open(cracked_file_path, 'w') as f:
        json.dump(existing_data, f, indent=2)

def crack_all_handshakes(wordlist):
    handshake_dir = "/opt/EvilPiG/wifite3/hs"
    
    for filename in os.listdir(handshake_dir):
        if filename.endswith(".cap"):  # Supondo que os arquivos de handshake tenham extensão .cap
            bssid = filename.split('_')[2].replace('-', ':')  # Extrai o BSSID do nome do arquivo (ajuste conforme necessário)
            print(f"Quebrando a senha para: {filename} com BSSID: {bssid}")
            crack_handshake(filename, bssid, wordlist)

def main():
    wordlist = '/opt/EvilPiG/wifite3/senhas.txt'

    if len(sys.argv) == 3:
        handshake_file = sys.argv[1]
        bssid = sys.argv[2]
        crack_handshake(handshake_file, bssid, wordlist)
    else:
        print("Nenhum argumento fornecido. Tentando quebrar todas as senhas na pasta hs...")
        crack_all_handshakes(wordlist)

if __name__ == "__main__":
    main()