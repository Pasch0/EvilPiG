import os
import subprocess
import string
import logging
import shutil
import time

# Configurações de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class HandshakeProcessor:
    def __init__(self):
        self.handshake_dir = '/opt/EvilPiG/hs'
        self.hashies_dir = '/opt/EvilPiG/hashies'
        self.timeout = 10  # Timeout em segundos para subprocessos
        self.processed_files_log = '/opt/EvilPiG/processed_files.log'  # Arquivo para registrar os arquivos já processados
        self.processed_files = self.load_processed_files()

    def load_processed_files(self):
        """Carrega a lista de arquivos já processados a partir do log."""
        if not os.path.exists(self.processed_files_log):
            return set()
        with open(self.processed_files_log, 'r') as file:
            return set(line.strip() for line in file)

    def save_processed_file(self, filename):
        """Salva o nome do arquivo processado no log."""
        with open(self.processed_files_log, 'a') as file:
            file.write(filename + '\n')
        self.processed_files.add(filename)

    def on_handshake(self, filename):
        todelete = 0
        handshakeFound = 0

        try:
            # Verifica se o arquivo possui handshake
            result = subprocess.run(('/usr/bin/aircrack-ng ' + filename + ' | grep "1 handshake"'),
                                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=self.timeout)
            output = result.stdout.decode('utf-8')
            logging.info(f"Resultado do Aircrack-ng para {filename}:\n{output}")

            if "1 handshake" in output:
                handshakeFound = 1
                logging.info(f"[AircrackOnly] Handshake encontrado no arquivo {filename}")

            if handshakeFound == 0:
                # Verifica se o arquivo possui PMKID
                result = subprocess.run(('/usr/bin/aircrack-ng ' + filename + ' | grep "PMKID"'),
                                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=self.timeout)
                output = result.stdout.decode('utf-8')
                logging.info(f"Resultado do Aircrack-ng para {filename} (PMKID):\n{output}")

                if "PMKID" in output:
                    logging.info(f"[AircrackOnly] PKMID encontrado no arquivo {filename}")
                    self.move_to_hashies(filename)
                else:
                    todelete = 1

            # Remove o arquivo caso não contenha handshake nem PMKID
            if todelete == 1:
                os.remove(filename)
                logging.warning(f"Arquivo {filename} removido, não contém PKMID nem Handshake.")

        except subprocess.TimeoutExpired:
            logging.error(f"Erro: O comando aircrack-ng para o arquivo {filename} excedeu o tempo limite de {self.timeout} segundos.")
            os.remove(filename)
            logging.warning(f"Arquivo {filename} removido devido ao timeout.")

        except Exception as e:
            logging.error(f"Erro ao processar o arquivo {filename}: {e}")
            os.remove(filename)
            logging.warning(f"Arquivo {filename} removido devido a erro de leitura ou processamento.")

        # Marca o arquivo como processado
        self.save_processed_file(filename)

    def move_to_hashies(self, filename):
        try:
            if not os.path.exists(self.hashies_dir):
                os.makedirs(self.hashies_dir)
            destination = os.path.join(self.hashies_dir, os.path.basename(filename))
            shutil.move(filename, destination)
            logging.info(f"Arquivo {filename} movido para a pasta {self.hashies_dir}.")
        except Exception as e:
            logging.error(f"Erro ao mover o arquivo {filename}: {e}")

    def process_pcaps(self):
        # Processa todos os arquivos .pcap no diretório de handshakes
        for filename in os.listdir(self.handshake_dir):
            file_path = os.path.join(self.handshake_dir, filename)
            if file_path.endswith(".pcap") and os.path.isfile(file_path):
                if file_path in self.processed_files:
                    logging.info(f"Arquivo {filename} já processado, ignorando.")
                    continue
                logging.info(f"Iniciando a verificação do arquivo {filename}.")
                self.on_handshake(file_path)

if __name__ == "__main__":
    processor = HandshakeProcessor()

    # Loop infinito para rodar a cada 15 segundos
    while True:
        processor.process_pcaps()
        logging.info("Aguardando 15 segundos antes de verificar novamente...")
        time.sleep(5)

