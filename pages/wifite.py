import streamlit as st
import pandas as pd
import json
import re
import os
import subprocess
from datetime import datetime
import threading

def clean_log_file(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            log_content = f.read()

        # Remove caracteres de controle e sequências de escape
        cleaned_content = re.sub(r'\x1b\[[0-?9;]*[mK]', '', log_content)

        # Salva o conteúdo limpo em um novo arquivo
        with open(output_file, 'w') as f:
            f.write(cleaned_content)

        print(f"Log limpo salvo em: {output_file}")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

# Defina os caminhos dos arquivos
input_log_file = '/opt/EvilPiG/wifite3/wifite.log'
output_log_file = '/opt/EvilPiG/wifite3/cleaned_wifite.log'

# Configuração da página
st.set_page_config(page_title="Wifite3 Dashboard", page_icon="🔗")

# Título do aplicativo
st.title("Dashboard Wifite3")

# Função para carregar redes invadidas do arquivo cracked.txt
def load_cracked_networks():
    try:
        with open('/opt/EvilPiG/wifite3/cracked.txt', 'r') as f:
            networks = json.load(f)
        
        # Converta a data de epoch para datetime
        for network in networks:
            if 'date' in network and isinstance(network['date'], int):
                network['date'] = datetime.fromtimestamp(network['date']).strftime('%Y-%m-%d %H:%M:%S')
        
        return pd.DataFrame(networks)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

# Função para carregar o conteúdo do wifite.log
def load_wifite_log():
    try:
        log_content = load_cleaned_wifite_log()
        return log_content
    except Exception as e:
        st.error(f"Erro ao carregar log: {e}")
        return ""

def load_cleaned_wifite_log():
    clean_log_file(input_log_file, output_log_file)
    with open(output_log_file, 'r') as f:
        return f.read()

# Função para listar handshakes capturados
def list_handshakes():
    try:
        handshake_dir = '/opt/EvilPiG/wifite3/hs/'
        handshakes = os.listdir(handshake_dir)
        handshake_list = []
        
        for handshake in handshakes:
            if handshake.startswith('handshake_') and handshake.endswith('.cap'):
                # Extrair nome da rede e data do nome do arquivo
                parts = handshake[10:-4].split('_')
                network_name = '_'.join(parts[:-1])
                date_str = parts[-1].replace('T', ' ').replace('-', '/')
                handshake_list.append({
                    'Network': network_name,
                    'Date': date_str,
                    'File': handshake,
                    'Cracked': False,
                    'Attempted': False
                })
        
        return pd.DataFrame(handshake_list)
    except Exception as e:
        st.error(f"Erro ao listar handshakes: {e}")
        return pd.DataFrame()

# Função para quebrar handshake usando o script crack_passwords.py
def run_crack_script(handshake_file, bssid):
    command = f"python3 /opt/EvilPiG/crack_passwords.py {handshake_file} {bssid}"
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Criação das abas
tab1, tab2, tab3 = st.tabs(["Redes Invadidas", "Log do Wifite", "Handshakes Capturados"])

# Aba 1: Tabela de Redes Invadidas
with tab1:
    st.subheader("Tabela de Redes Invadidas")
    cracked_networks_df = load_cracked_networks()
    
    if not cracked_networks_df.empty:
        st.dataframe(cracked_networks_df)
    else:
        st.write("Nenhuma rede invadida encontrada.")

# Aba 2: Conteúdo do Log
with tab2:
    st.subheader("Conteúdo do Log do Wifite")
    
    if st.button("Ver log"):
        log_content = load_wifite_log()

        if log_content:
            st.code(log_content)

        if st.button("Atualizar Log"):
            st.rerun()
            log_content = load_wifite_log()
            st.code(log_content)

# Aba 3: Handshakes Capturados
with tab3:
    st.subheader("Handshakes Capturados")
    handshakes_df = list_handshakes()
    
    if not handshakes_df.empty:
        st.dataframe(handshakes_df)
        
        # Selecionar handshake para quebrar
        selected_handshake = st.selectbox("Selecione o handshake para quebrar", handshakes_df['File'].tolist())
        
        if st.button("Quebrar Handshake"):
            selected_row = handshakes_df[handshakes_df['File'] == selected_handshake].iloc[0]
            bssid = selected_row['Network'].split('_')[-1]  # Supondo que o BSSID está no final do nome da rede
            
            handshakes_df.loc[handshakes_df['File'] == selected_handshake, 'Attempted'] = True
            
            # Executar script de quebra de senha em segundo plano usando threading
            threading.Thread(target=run_crack_script, args=(selected_handshake, bssid)).start()
            
            st.success("Quebra de handshake iniciada. Aguarde o resultado.")
    else:
        st.write("Nenhum handshake capturado encontrado.")