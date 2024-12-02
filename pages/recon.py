import streamlit as st
import subprocess
import json
import os
from datetime import datetime

# Cria o diretório de histórico se não existir
history_dir = 'scan_history'
if not os.path.exists(history_dir):
    os.makedirs(history_dir)

# Função para executar o masscan em uma sessão tmux
def run_masscan(ip_range, ports, rate, sv, sc):
    session_name = "masscan_session"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{history_dir}/masscan_{ip_range.replace('/', '_')}_{ports.replace(',', '_')}_{timestamp}.txt"
    
    command = f"tmux new-session -d -s {session_name} 'masscan {ip_range} -p{ports} -T{rate}"
    if sv:
        command += " --banners"
    if sc:
        command += " --script"
    command += f" -oN {output_file}'"  # Salva a saída em um arquivo
    
    subprocess.run(command, shell=True)
    return output_file

# Função para executar o nmap em uma sessão tmux
def run_nmap(ip_range, ports, sv, sc):
    session_name = "nmap_session"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{history_dir}/nmap_{ip_range.replace('/', '_')}_{ports.replace(',', '_')}_{timestamp}.txt"
    
    command = f"tmux new-session -d -s {session_name} 'nmap {ip_range} -p{ports}"
    if sv:
        command += " -sV"
    if sc:
        command += " -sC"
    command += f" -oN {output_file}'"  # Salva a saída em um arquivo
    
    subprocess.run(command, shell=True)
    return output_file

# Função para verificar se há scans em andamento
def check_running_scans():
    masscan_running = subprocess.run("tmux has-session -t masscan_session", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    nmap_running = subprocess.run("tmux has-session -t nmap_session", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return masscan_running.returncode == 0, nmap_running.returncode == 0

# Função para salvar o histórico de scans
def save_history(scan_result):
    if not os.path.exists('scan_history.json'):
        with open('scan_history.json', 'w') as f:
            json.dump([], f)
    
    with open('scan_history.json', 'r+') as f:
        history = json.load(f)
        history.append(scan_result)
        f.seek(0)
        json.dump(history, f)

# Função para carregar o histórico de scans
def load_history():
    if os.path.exists('scan_history.json'):
        with open('scan_history.json', 'r') as f:
            return json.load(f)
    return []

# Função para encerrar uma sessão tmux
def kill_tmux_session(session_name):
    subprocess.run(f"tmux kill-session -t {session_name}", shell=True)

# Interface do Streamlit
st.title("Recon Tool: Masscan & Nmap")

# Verifica se há scans em andamento
masscan_running, nmap_running = check_running_scans()

if masscan_running:
    st.warning("Um scan do Masscan está em andamento.")
if nmap_running:
    st.warning("Um scan do Nmap está em andamento.")

# Criação das abas
tabs = st.tabs(["Masscan", "Nmap", "Scan History"])

# Aba para Masscan
with tabs[0]:
    st.header("Masscan")
    ip_range = st.text_input("IP Range (ex: 192.168.1.0/24)", key="ip_range_masscan", value="192.168.1.0/24")
    ports = st.text_input("Ports (ex: 80,443)", key="ports_masscan", value="80,443")
    rate = st.selectbox("Rate (T)", [1, 2, 3, 4, 5])
    
    # Checkboxes com chaves únicas
    sv = st.checkbox("Enable Service Version Detection (-sV)", key="sv_masscan")
    sc = st.checkbox("Enable Script Scan (-sC)", key="sc_masscan")
    
    if st.button("Run Masscan"):
        output_file = run_masscan(ip_range, ports, rate, sv, sc)
        save_history(output_file)  # Salva o histórico com o nome do arquivo gerado
        st.success(f"Scan do Masscan iniciado. Saída salva em: {output_file}")

# Aba para Nmap
with tabs[1]:
    st.header("Nmap")
    ip_range_nmap = st.text_input("IP Range (ex: 192.168.1.0/24) for Nmap", key="ip_range_nmap", value="192.168.1.0/24")
    ports_nmap = st.text_input("Ports (ex: 80,443) for Nmap", key="ports_nmap", value="80,443")
    
    # Checkboxes com chaves únicas
    sv_nmap = st.checkbox("Enable Service Version Detection (-sV)", key="sv_nmap")
    sc_nmap = st.checkbox("Enable Script Scan (-sC)", key="sc_nmap")
    
    if st.button("Run Nmap"):
        output_file_nmap = run_nmap(ip_range_nmap, ports_nmap, sv_nmap, sc_nmap)
        save_history(output_file_nmap)  # Salva o histórico com o nome do arquivo gerado
        st.success(f"Scan do Nmap iniciado. Saída salva em: {output_file_nmap}")

# Aba para visualizar histórico de scans
with tabs[2]:
    st.header("Scan History")
    
    # Carrega o histórico de scans
    history = load_history()
    
    # Select box para escolher um scan do histórico
    selected_scan_file = st.selectbox("Selecione um scan:", history)

    # Exibe o conteúdo do arquivo selecionado
    if selected_scan_file:
        with open(selected_scan_file, 'r') as file:
            content = file.read()
            st.code(content)  # Mostra o conteúdo no formato de código
    
    for i, scan in enumerate(history):
        st.write(f"Scan {i + 1}: {scan}")
        
        if st.button(f"Delete Scan {i + 1}", key=f"delete_{i}"):
            history.pop(i)
            with open('scan_history.json', 'w') as f:
                json.dump(history, f)
            st.experimental_rerun()

# Botão para encerrar sessões ativas
if masscan_running and st.button("Encerrar Masscan"):
    kill_tmux_session("masscan_session")
    st.success("Sessão do Masscan encerrada.")

if nmap_running and st.button("Encerrar Nmap"):
    kill_tmux_session("nmap_session")
    st.success("Sessão do Nmap encerrada.")