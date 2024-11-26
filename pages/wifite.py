import streamlit as st
import pandas as pd
import json
import re

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

# Função para carregar redes invadidas do arquivo cracked.json
def load_cracked_networks():
    try:
        with open('/opt/EvilPiG/wifite3/cracked.txt', 'r') as f:
            networks = json.load(f)
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

# Criação das abas
tab1, tab2 = st.tabs(["Redes Invadidas", "Log do Wifite"])

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
