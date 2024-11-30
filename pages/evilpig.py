import streamlit as st
import psutil  # To get system information
import subprocess  # To run system commands
import os  # To manipulate files
from time import sleep

# Page configuration
st.set_page_config(page_title="Evil Pig 🐷", page_icon="")

st.title("EvilPig 🐷")

# Banner
#banner = f"""
#    ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░      ░▒▓███████▓▒░░▒▓█▓▒░░▒▓██████▓▒░  
#    ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
#    ░▒▓█▓▒░       ░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░        
#    ░▒▓██████▓▒░  ░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓███████▓▒░░▒▓█▓▒░▒▓█▓▒▒▓███▓▒░ 
#    ░▒▓█▓▒░        ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
#    ░▒▓█▓▒░        ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
#    ░▒▓████████▓▒░  ░▒▓██▓▒░  ░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓██████▓▒░  
#                                                                               
#                                                    ▓▓▓███▓▓▓                       
#                     ░▒░                        ░▓▓███▓░▒░▒▓██▓                     
#                  ▓▓█████▓▓        ░▒▒▒▒▒▒▒▒░ ▒▓███░░░███░░░░██▓▒                   
#               ░▒▓█░░░░░░███▓▒▓▓▓████████████████░░░█████░░░░█████▓▒                
#           ▒▓██████░░░░░░░░██████▓██▒░░░░░░░░░░▒░░░██▒███░░░░██░░▓██▓▓              
#           ▓███▓▒██░░░███░░░░░░░░▒█░░░░░░░░░░░░░░░██▒▒███░░░░░▓░░▒████▓             
#           ▓██▓░░█▒░░░████░░░░░░░▒▒░░░░░░░░░░░░░░░██▒▒███░░░░░░░░▓███▓              
#          ░▓██▒░░░░░░░██▓█░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▓███░░░6░░░████▓              
#          ▒██▒░░░6░░░▓██▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒███░░░░░░▒████▒              
#          ▒██▒▒░░░░░░██▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓███▒░░░▒▓███▓░              
#          ▒██▒▒░░░░░██▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓████▓▒▒▓███▓               
#          ▒██▓▒▒▒░▓███▓▓░░░░░░░░░░░░6░░░░░░░░░░░░▓██▒▒▒▒▒▒██████▓███▓▒              
#          ░███▓▒████▓▒▒▓██░░░░░░░░░░░░░░░░░░░░▒████▒▒▒▒▒▒▒▒▒█████████▓              
#           ▓████████▒▒▒▒█▓█░░░▒▓░░░░░░▓▓░░░░▒█▓▓▓█▓▒▒▒▒░▒▒▒▒██▓██████▓              
#           ▓█████▓▓█▒▒▒▓█▓▓█░░░░░░░░░░░░░░▒██▓▓▓███▓▒░░░▒▒▒▒▒██▓▓░▒▓▓▓▓             
#           ░▓██▓▓▓█▒▒▒▒▒▓▓▓▓█▓░░████░░░░▓███▓▓▓▓█▒▒▒░░░░░▒▒▒▒▒███▓                  
#            ▓▓▒ ░▓█▒▒░░▒▒▓█████████████████████▓▒▒░░░░░░░░▒▒▒▒▒▓██▓░                
#                ▓█▒▒░░░░░░░░░░████▓░░▒█▓▒▒▒▒▒▒▒▒░░░░░░░░░░░▒▒▒▒▒▒███▓               
#              ░▓██▒░░░░░░▓░░███░▓░░░█▒░░░░░░░░░▓▓░░░░░░░░░░░░▒▒▒▒▒▒██▓▓             
#             ▒▓██▒░░░░░░█▒▓█▒▒▒█░░▓▒░░░░░░░░▓████▓░░░░░░░░░░░░░▒▒▒▒▒███▓            
#            ▒▓██▒▒░░░░░█▓█▒▒▓█▒▒▓▓░░░░░░░░░█▓░  ░██░░░░░░░░░░░░░▒▒▒▒▒███▒           
#           ░▓██▒▒░░░░▓█▒██▒▒▒██▓▒▒▓█▒░░░░▓▒ ▒ ░▓░███░░░░░░░░░░░░░▒▒▒▒███▓           
#           ▓██▓▒░░░░░█▒▒▓▒▓█▓▒█▓▒▒▒██░░▒    ▒    ░██░░░░░░░░░░░░░▒▒▒▒▒███▒          
#          ░▓██▒▒░░░░░██▓███████▓▓████░ ▒██▒▒▓█████▓█░░░░░░░░░░░░░▒▒▒▒▒███▒          
#          ▒███▒░░░░░░░▓█░░░░░░░░▒▓░░███░░░░██░░██▓░█░░░░░░░░░░░░░▒▒▒▒▓███▒          
#          ░▓██▒░░░░░░░▓█▓██▒▒▓▓█▓░░░░░░░░░░░░░░░░███░░░░░░░░░░░░░▒▒▒▒████▒          
#           ▓██▒▒░░░░░░░░░░█▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▓███▓           
#           ░▓██▒▒░░░░░░░░░▒█▓▒▒▒░░░░░░░░░▒▒░░░░░░░░░░░░▒▒░░░░░▒▒▒▒▒▓███▓░           
#            ▒▓██▒▒▒░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░▒▒▒░░░▒▒▒▒▒▒▒████▓▒            
#             ▒▓███▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█████▓░             
#               ▓▓█████▒▒▒▒▒▓█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒▒▒███████▓▒               
#                 ░▒▓▓██▒▒▒▒▒▒██▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓███▒▒▒▒▒▒▒▒████▓▒                  
#                     ░▓██████████████▓▓▓▓▓██████▓▒▒▒▒▒▒▒▓█████▓▒                    
#        by: Pasch0      ▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████▓▓▓▒                       
#
#                              --------------------------
#                      ---= FREE & OPEN SOURCE PENTEST TOOL =---
#                              --------------------------
#
#                                      AVISO LEGAL
#               ___________________________________________________________
#              |                                                           |
#              | Esta ferramenta foi desenvolvida para fins educacionais   |
#              | podendo ser utilizada em laboratórios e ambientes contro- |
#              | lados. A realização de ataques a ambientes não autorizados|
#              | pode ser considerado crime. O autor não se responsabiliza |
#              | pelo uso indevido desta ferramenta.                       |
#              |___________________________________________________________|
#    """

banner = """
░▒▓████▓▒ ░▒█▓▒░░▒▓▓▒░  ░▒▓▒░▒▓▒░     ░▒▓███▓▒░░▒▓▒░░▒▓██▓▒░  
░▒▒░      ░▒▓▓▒░░▒▓▓▒░  ░▒▓▒░▒▓▒░     ░▒▓▒░░▒▓▒░▒▓▒░▒▓▒░░▒▓▒░ 
░▒▒░      ░▒▓▓▒░░▒▓▓▒░  ░▒▓▒░▒▓▒░     ░▒▓▒░░▒▓▒░▒▓▒░▒▓▒░        
░▒▓██▓▒░   ░▒▓▓▒▒▓▓▒░   ░▒▓▒░▒▓▒░     ░▒▓███▓▒░░▒▓▒░▒▓▒░▓█▓▒░ 
░▒▒░        ░▒█▓▓█▓▒    ░▒▓▒░▒▓▒░     ░▒▓▒░    ░▒▓▒░▒▓▒░░▒▓▒░ 
░▒▒░         ▒▓▓▓█▒░    ░▒▓▒░▒▓▒░     ░▒▓▒░    ░▒▓▒░▒▓▒░░▒▓▒░ 
░▒▓███▓▒░     ▒▓█▓▒     ░▒▓▒░▒▓█████▓▒░▒▓▒░    ░▒▓▒░░▒███▓▒░         

                         ...     .......                      
                  ..-+#########################+++-..         
             ..+#######################################+...#+.
 .....-####+##############################################+#++
 .-########################################################+. 
  .-########################################################. 
    .+######################################################. 
...-+######################################################+. 
###########################################################-. 
###########################################################.  
..-++####################################################+.   
     .....--+###########################################+.    
               .#######..--+++#########++-....+#########+.    
               .+#####-.                      .+###.+###+.    
               .+#++##.                        .##-..+##-.    
               .##.-#+                         .##.  -##.     
               -+..##.                        .+-.. .+#+.     
                  ....                              ...       
                                                              
                    --------------------------
            ---= FREE & OPEN SOURCE PENTEST TOOL =---
                    --------------------------
                            AVISO LEGAL
   ___________________________________________________________
  |                                                           |
  | Esta ferramenta foi desenvolvida para fins educacionais   |
  | podendo ser utilizada em laboratórios e ambientes contro- |
  | lados. A realização de ataques a ambientes não autorizados|
  | pode ser considerado crime. O autor não se responsabiliza |
  | pelo uso indevido desta ferramenta.                       |
  |___________________________________________________________|
"""

st.code(banner)

# Função para listar todas as interfaces de rede disponíveis usando iwconfig
def get_wifi_interfaces():
    result = subprocess.run(['iwconfig'], capture_output=True, text=True)
    interfaces = []
    for line in result.stdout.splitlines():
        if 'IEEE 802.11' in line:
            iface = line.split()[0]
            interfaces.append(iface)
    return interfaces

# Função para iniciar o ataque de spoofing no tmux
def start_spoofing(interface):
    tmux_session_name = "evilpig-wifi-spoofing"
    # Verifica se a sessão já está em execução e encerra se necessário
    subprocess.run(["tmux", "kill-session", "-t", tmux_session_name], stderr=subprocess.DEVNULL)

    # Inicia uma nova sessão tmux com o script de spoofing
    subprocess.run(["tmux", "new-session", "-d", "-s", tmux_session_name, f"python3 /opt/EvilPiG/wifispoof.py {interface}"])
    return f"Ataque de spoofing iniciado na interface {interface}."

# Função para parar o ataque de spoofing no tmux
def stop_spoofing():
    tmux_session_name = "evilpig-wifi-spoofing"
    subprocess.run(["tmux", "kill-session", "-t", tmux_session_name], stderr=subprocess.DEVNULL)
    return "Ataque de spoofing parado."

# Listar interfaces de rede disponíveis
wifi_interfaces = get_wifi_interfaces()

# Se wlan0 estiver na lista, mas não for a única interface, remova-a e selecione a outra interface como padrão
if 'wlan0' in wifi_interfaces:
    if len(wifi_interfaces) > 1:
        wifi_interfaces.remove('wlan0')

selected_interface = st.selectbox("Selecione a interface Wi-Fi:", wifi_interfaces)

st.divider()

# Função para coletar temperaturas
def get_temperatures():
    result = subprocess.run(['sensors'], capture_output=True, text=True)
    
    cpu, gpu, ddr, ve = None, None, None, None
    for line in result.stdout.split('\n\n'):
        if 'cpu' in line:
            cpu = line.split('+')[1].split(' ')[0]
        elif 'gpu' in line:
            gpu = line.split('+')[1].split(' ')[0]
        elif 'ddr' in line:
            ddr = line.split('+')[1].split(' ')[0]
        elif 've' in line:
            ve = line.split('+')[1].split(' ')[0]
        
    return cpu, gpu, ddr, ve

# Função para obter uso de recursos
def get_resource_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    
    return cpu_usage, ram_usage, disk_usage

# Impressão das informações de uso de recursos do sistema
cpu_usage, ram_usage, disk_usage = get_resource_usage()
cpu_temp, gpu_temp, ddr_temp, ve_temp = get_temperatures()

st.subheader("Uso de Recursos do Sistema")
col1, col2 = st.columns(2)
try:
    col1.metric("**Uso de CPU:**", f"{cpu_usage}%", "4%")
    col2.metric(f"**Temperatura da CPU:**", f"{cpu_temp}", "1.2 °C")
except:
    pass
try:
    col1.metric(f"**Uso de RAM:**", f"{ram_usage}%", "-1%")
    col2.metric(f"**Temperatura da RAM:**", f"{ddr_temp}", "6%")
except:
    pass
try:
    col1.metric(f"**Uso de Disco:**", f"{disk_usage}%", "6%")
    col2.metric(f"**Temperatura VE:**", f"{ve_temp}", "1.2 °C")
except:
    pass

# Função para verificar o status do serviço 'evilpig-wifi'
def check_evilpig_wifi_status(number):
    attack_type = {
        1: 'wps',
        2: 'wpa',
        3: 'mix',
        4: 'spoofing',
        5: 'ble-scan'
    }
    if number != 5:
        try:
            output = subprocess.check_output(['tmux', 'list-sessions']).decode('utf-8')
            return f'evilpig-wifi-{attack_type[number]}' in output  # Verifica corretamente a sessão do ataque
        except subprocess.CalledProcessError:
            return False
    else:
        try:
            return 'Active: active (running)'in subprocess.run(['systemctl', 'status', 'hci-eye.service'], capture_output=True, text=True).stdout.strip()
        except subprocess.CalledProcessError:
            return False
    
# criar função que inicia ataque ble-scan
def start_ble_scan(interface):
    stop_ble_scan()
    subprocess.run(['systemctl', 'start', 'hci-eye.service'])
    return f"ble-scan iniciado na interface {interface}."

# criar função que para ataque ble-scan
def stop_ble_scan():
    subprocess.run(['systemctl', 'stop', 'hci-eye.service'])
    return "ble-scan parado."

# Funções para controlar o serviço 'evilpig-wifi'
def start_evilpig_wifi(attack):
    for i in range(1, 4):
        if check_evilpig_wifi_status(i):
            stop_evilpig_wifi(i)
    
    process = subprocess.Popen(['bash', '/opt/EvilPiG/evilpig-wifi.sh', str(attack)])
    with open('/tmp/evilpig-wifi.pid', 'w') as f:
        f.write(str(process.pid))

def stop_evilpig_wifi(number):
    attack_type = {
        1: 'wps',
        2: 'wpa',
        3: 'mix'
    }
    
    if os.path.exists('/tmp/evilpig-wifi.pid'):
        with open('/tmp/evilpig-wifi.pid', 'r') as f:
            pid = int(f.read().strip())
            try:
                os.kill(pid, 15)  # Envia um sinal SIGTERM para parar o processo
            except ProcessLookupError:
                pass
    
    if os.path.exists('/tmp/evilpig-wifi.pid'):
        os.remove('/tmp/evilpig-wifi.pid')
    
    if check_evilpig_wifi_status(number):
        subprocess.call(['tmux', 'kill-session', '-t', f'evilpig-wifi-{attack_type[number]}'])

# Impressão do status do serviço evilpig-wifi
st.subheader("Status do Ataque Automático")

# Função para gerar círculo colorido
def colored_circle(status):
    return "🟢" if status else "🔴"

# Serviço evilpig-wifi-WPS
with st.expander(f"{colored_circle(check_evilpig_wifi_status(1))} WPS Pixie Dust"):
    if check_evilpig_wifi_status(1):
        if st.button("Parar", key="stop_evilpig_wifi-wps"):
            stop_evilpig_wifi(1)
            st.rerun()
    else:
        if st.button("Iniciar", key="start_evilpig_wifi-wps"):
            start_evilpig_wifi(1)
            st.rerun()

# Serviço evilpig-wifi-WPA/WPA2 Handshake Cracking
with st.expander(f"{colored_circle(check_evilpig_wifi_status(2))} WPA/WPA2 Handshake Cracking"):
    if check_evilpig_wifi_status(2):
        if st.button("Parar", key="stop_evilpig_wifi-wpa"):
            stop_evilpig_wifi(2)
            st.rerun()
    else:
        if st.button("Iniciar", key="start_evilpig_wifi-wpa"):
            start_evilpig_wifi(2)
            st.rerun()

# Serviço evilpig-wifi-WPA/WPS Mixed Attack
with st.expander(f"{colored_circle(check_evilpig_wifi_status(3))} WPA/WPS Mixed Attack"):
    if check_evilpig_wifi_status(3):
        if st.button("Parar", key="stop_evilpig_wifi-mix"):
            stop_evilpig_wifi(3)
            st.rerun()
    else:
        if st.button("Iniciar", key="start_evilpig_wifi-mix"):
            start_evilpig_wifi(3)
            st.rerun()

# Novo expander para ataque de spoofing Wi-Fi
with st.expander(f"{colored_circle(check_evilpig_wifi_status(4))} Ataque de Spoofing Wi-Fi"):
    if check_evilpig_wifi_status(4):
        if st.button("Parar Spoofing", key="stop_spoofing"):
            stop_spoofing()
            st.rerun()
    else:
        if st.button("Iniciar Spoofing", key="start_spoofing"):
            result = start_spoofing(selected_interface)
            st.success(result)
            st.rerun()

with st.expander(f"{colored_circle(check_evilpig_wifi_status(5))} Scan Bluetooth"):
    if check_evilpig_wifi_status(5):
        if st.button("Parar ble-scan", key="stop_ble-scan"):
            stop_ble_scan()
            st.rerun()
    else:
        if st.button("Iniciar ble-scan", key="start_ble-scan"):
            result = start_ble_scan(selected_interface)
            st.success(result)
            st.rerun()

st.divider()

st.subheader("Controle do Sistema")

# Botões para reiniciar e desligar o sistema
with st.container():
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col6:
        if st.button("Reiniciar"):
            subprocess.run(["sudo", "reboot"])
    
    with col1:
        if st.button("Desligar"):
            subprocess.run(["sudo", "poweroff"])

st.divider()

# Impressão das instruções para navegação final
st.write("Use o menu à esquerda para navegar entre as páginas.")