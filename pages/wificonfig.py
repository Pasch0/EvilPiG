import streamlit as st
import subprocess

# Função para verificar e ativar o adaptador Bluetooth hci0
def check_and_activate_adapter():
    try:
        # Verifica o status do adaptador hci0
        result = subprocess.run(["python3", "cracked2suppliacnt.py"], capture_output=True, text=True)
    except Exception as e:
        st.error(f"Erro ao verificar ou ativar o adaptador: {str(e)}")

# Função para ler o arquivo de configuração
def read_wifi_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return ""

# Função para salvar as alterações no arquivo de configuração
def save_wifi_config(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        st.success("Alterações salvas com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar o arquivo: {e}")

# Função para listar redes disponíveis usando wpa_cli
def list_available_networks(interface):
    try:
        result = subprocess.run(["wpa_cli", "-i", interface, "list_networks"], capture_output=True, text=True)
        networks = result.stdout.splitlines()[1:]  # Ignorar cabeçalho
        return [line.split()[1] for line in networks if line]  # Retornar apenas SSIDs
    except Exception as e:
        st.error(f"Erro ao listar redes: {e}")
        return []

# Função para conectar-se a uma rede específica
def connect_to_network(interface, network_id):
    try:
        subprocess.run(["ifconfig", interface, "down"], check=True)
        subprocess.run(["iwconfig", interface, "mode", "managed"], check=True)
        subprocess.run(["ifconfig", interface, "up"], check=True)
        subprocess.run(["wpa_cli", "-i", interface, "select_network", str(network_id)], check=True)
        subprocess.run(["sudo", "dhclient", interface], check=True)  # Obter DHCP
        st.success(f"Conectado à rede com ID {network_id}.")
    except Exception as e:
        st.error(f"Erro ao conectar à rede: {e}")

# Página de configuração Wi-Fi
st.title("Configuração de Redes Wi-Fi")

# Criar abas
tab1, tab2, tab3 = st.tabs(["Configuração WLAN0", "Configuração USB de Ataque", "Conectar a Rede"])

# Aba para configuração WLAN0
with tab1:
    st.header("Configuração da Interface WLAN0")
    
    # Ler o conteúdo do arquivo wpa_supplicant.conf
    current_content_wlan0 = read_wifi_config('/etc/wpa_supplicant/wpa_supplicant.conf')

    # Editor de texto para editar o conteúdo do arquivo
    edited_content_wlan0 = st.text_area("Edite o arquivo wpa_supplicant.conf:", current_content_wlan0, height=300)

    # Botão para salvar as alterações
    if st.button("Salvar Alterações WLAN0"):
        save_wifi_config('/etc/wpa_supplicant/wpa_supplicant.conf', edited_content_wlan0)

    # Exibir o conteúdo atual do arquivo
    st.subheader("Conteúdo Atual do Arquivo:")
    st.code(current_content_wlan0, language='plaintext')

# Aba para configuração USB de ataque
with tab2:
    check_and_activate_adapter()
    st.header("Configuração da Interface USB de Ataque")
    
    # Ler o conteúdo do arquivo wpa_supplicant com -attack.conf
    current_content_usb = read_wifi_config('/etc/wpa_supplicant/wpa_supplicant-attack.conf')

    # Editor de texto para editar o conteúdo do arquivo
    edited_content_usb = st.text_area("Edite o arquivo wpa_supplicant-attack.conf:", current_content_usb, height=300)

    # Botão para salvar as alterações
    if st.button("Salvar Alterações USB"):
        save_wifi_config('/etc/wpa_supplicant/wpa_supplicant-attack.conf', edited_content_usb)

    # Exibir o conteúdo atual do arquivo
    st.subheader("Conteúdo Atual do Arquivo:")
    st.code(current_content_usb, language='plaintext')

# Aba para conectar a uma rede específica
with tab3:
    st.header("Conectar a uma Rede Wi-Fi")

    interface = "wlx0036765525cc"
    
    # Listar redes disponíveis
    networks = list_available_networks(interface)
    
    if networks:
        selected_network = st.selectbox("Selecione uma Rede:", networks)

        if st.button("Conectar"):
            network_id = networks.index(selected_network)  # Obter ID da rede selecionada
            connect_to_network(interface, network_id)