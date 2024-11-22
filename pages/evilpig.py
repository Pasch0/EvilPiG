import streamlit as st
import psutil  # To get system information
import subprocess  # To run system commands
import os  # To manipulate files

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
#
░▒▓████▓▒ ░▒█▓▒░░▒▓▓▒░  ░▒▓▒░▒▓▒░     ░▒▓███▓▒░░▒▓▒░░▒▓██▓▒░  
░▒▒░      ░▒▓▓▒░░▒▓▓▒░  ░▒▓▒░▒▓▒░     ░▒▓▒░░▒▓▒░▒▓▒░▒▓▒░░▒▓▒░ 
░▒▒░      ░▒▓▓▒░░▒▓▓▒░  ░▒▓▒░▒▓▒░     ░▒▓▒░░▒▓▒░▒▓▒░▒▓▒░        
░▒▓██▓▒░   ░▒▓▓▒▒▓▓▒░   ░▒▓▒░▒▓▒░     ░▒▓███▓▒░░▒▓▒░▒▓▒░▓█▓▒░ 
░▒▒░        ░▒█▓▓█▓▒    ░▒▓▒░▒▓▒░     ░▒▓▒░    ░▒▓▒░▒▓▒░░▒▓▒░ 
░▒▒░         ▒▓▓▓█▒░    ░▒▓▒░▒▓▒░     ░▒▓▒░    ░▒▓▒░▒▓▒░░▒▓▒░ 
░▒▓███▓▒░     ▒▓█▓▒     ░▒▓▒░▒▓█████▓▒░▒▓▒░    ░▒▓▒░░▒███▓▒░         
                                     ▒▓▓▓▓▓▓▓▓▒          
           ▒▓▓▓▓▓▒                ░▓▓▓▓▒▒▓▓▒▒▒▓▓▒        
        ░▒▓▓▒▒▒▒▓▓▓▓░▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▓▓▓▓▒▒▒▓▓▓▓▓░     
     ▓▓▓▓▓▓▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▒▒▒▓▓▒▒▓▓▓▒   
    ░▓▓▓▒▒▓▒▒▒▓▓▓▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▓▓▓▒▒▒▒▒▒▒▓▓▓▓   
    ░▓▓▓▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▓▓▒▒▒▒▒▒▒▓▓▓▒   
    ▒▓▓▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█▓▒▒▒▒▒▓▓▓▓░   
    ▒▓▓▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▒▒▒▒▓▓▓▓░   
    ▒▓▓▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒▓▓▓▓░   
    ▒▓▓▓▒▒▓▓▓▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓░   
    ░▓▓▓▓▓▓▓▒▒▒▓▓▓▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▒   
     ▓▓▓▓▓▓▓▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▒▒▒▒▒▒▒▓▓▓▒▒▓▓▓▒  
     ░▓▓▓▓▓▓▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▒▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▓▓▓▒      
      ░  ▒▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓░    
        ▒▓▓▒▒▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓░  
       ▓▓▓▒▒▒▒▒▒▓▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓░ 
      ▓▓▓▒▒▒▒▒▒▓▓▓▒▓▓▒▒▓▒▒▒▒▒▒▒▓▓░░░▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓ 
     ▓▓▓▒▒▒▒▒▓▒▒▓▓▒▒▓▓▒▒▒▓▒▒▒▒░▒▓░▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓░
    ░▓▓▓▒▒▒▒▒▓▒▒▓▓▓▓▓▒▒▒▓▓▒▒▒▒▒▓▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▒
    ▒▓▓▓▒▒▒▒▒▒▓▓▒▒▒▒▒▒▓▓▒▒▒▓▒▒▒▒▒▒▒▓▓▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▒
    ░▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓░
     ▓▓▓▒▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓ 
     ░▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓░ 
      ░▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓░  
        ▒▓▓▓▓▓▓▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▒▓▓▓▓▓▓▓▓░    
           ░▒▓▓▓▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▓▓▓▓░       
              ░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░

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

# Function to collect temperatures
def get_temperatures():
    # Runs the command 'sensors' and collects the output
    result = subprocess.run(['sensors'], capture_output=True, text=True)

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

# Function to get resource usage
def get_resource_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    
    return cpu_usage, ram_usage, disk_usage

# Function to check the status of the service 'evilpig-wifi'
def check_evilpig_wifi_status(number):
    attack_type = {
        1: 'wps',
        2: 'wpa',
        3: 'mix'
    }
    try:
        output = subprocess.check_output(['tmux', 'list-sessions']).decode('utf-8')
        return f'evilpig-wifi-{attack_type[number]}' in output
    except subprocess.CalledProcessError:
        return False

# Functions to control the service 'evilpig-wifi'
def start_evilpig_wifi(attack):
    for i in range(1, 4):
        if check_evilpig_wifi_status(i):
            stop_evilpig_wifi(i)
        else:
            pass
    process = subprocess.Popen(['bash', '/opt/evilpig/evilpig-wifi.sh', str(attack)])
    with open('/tmp/evilpig-wifi.pid', 'w') as f:
        f.write(str(process.pid))

def restart_evilpig_wifi(attack):
    stop_evilpig_wifi(attack)
    start_evilpig_wifi(attack)

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
                os.kill(pid, 15)  # Sends a SIGTERM signal to stop the process
            except ProcessLookupError:
                pass
    
    if os.path.exists('/tmp/evilpig-wifi.pid'):
        os.remove('/tmp/evilpig-wifi.pid')
    
    if check_evilpig_wifi_status(number):
        subprocess.call(['tmux', 'kill-session', '-t', f'evilpig-wifi-{attack_type[number]}'])

st.divider()

# Prints resource usage information
cpu_usage, ram_usage, disk_usage = get_resource_usage()
cpu_temp, gpu_temp, ddr_temp, ve_temp = get_temperatures()

st.subheader("System Resource Usage")
col1, col2 = st.columns(2)
col1.metric("**CPU Usage:**", f"{cpu_usage}%", "4%")
col2.metric(f"**CPU Temperature:**", f"{cpu_temp}", "1.2 °C")
col1.metric(f"**RAM Usage:**", f"{ram_usage}%", "-1%")
col2.metric(f"**RAM Temperature:**", f"{ddr_temp}", "6%")
col1.metric(f"**Disk Usage:**", f"{disk_usage}%", "6%")
col2.metric(f"**VE Temperature:**", f"{ve_temp}", "1.2 °C")

st.divider()

# Prints status of evilpig-wifi service
st.subheader("Auto Attack Status")

with st.container():
    col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])  # Adjusts column widths

    # Service evilpig-wifi-WPS
    with col1:
        st.write("**WPS Pixie Dust**")
    
    with col2:
        if check_evilpig_wifi_status(1):
            st.markdown("<span style='color: green;'>Running</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color: red;'>Stopped</span>", unsafe_allow_html=True)

    with col3:
        if st.button("Start", key="start_evilpig-wifi-wps"):
            start_evilpig_wifi(1)
            st.rerun()
    with col4:
        if st.button("Stop", key="stop_evilpig_wifi-wps"):
            stop_evilpig_wifi(1)
            st.rerun()
    with col5:
        if st.button("Restart", key="restart_evilpig_wifi-wps"):
            restart_evilpig_wifi(1)
            st.rerun()

     # Service evilpig-wifi
    with col1:
        st.write("**WPA/WPA2 Handshake Cracking**")
    
    with col2:
        if check_evilpig_wifi_status(2):
            st.markdown("<span style='color: green;'>Running</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color: red;'>Stopped</span>", unsafe_allow_html=True)

    with col3:
        if st.button("Start", key="start_evilpig-wifi-wpa"):
            start_evilpig_wifi(2)
            st.rerun()
    with col4:
        if st.button("Stop", key="stop_evilpig_wifi-wpa"):
            stop_evilpig_wifi(2)
            st.rerun()
    with col5:
        if st.button("Restart", key="restart_evilpig_wifi-wpa"):
            restart_evilpig_wifi(2)
            st.rerun()

     # Service evilpig-wifi
    with col1:
        st.write("**WPA/WPS Mixed Attack**")
    
    with col2:
        if check_evilpig_wifi_status(3):
            st.markdown("<span style='color: green;'>Running</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color: red;'>Stopped</span>", unsafe_allow_html=True)

    with col3:
        if st.button("Start", key="start_evilpig-wifi-mix"):
            start_evilpig_wifi(3)
            st.rerun()
    with col4:
        if st.button("Stop", key="stop_evilpig_wifi-mix"):
            stop_evilpig_wifi(3)
            st.rerun()
    with col5:
        if st.button("Restart", key="restart_evilpig_wifi-mix"):
            restart_evilpig_wifi(3)
            st.rerun()

st.divider()

st.subheader("System Control")

# Buttons to restart and shutdown the system
with st.container():
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col6:
        if st.button("Reboot"):
            subprocess.run(["sudo", "reboot"])
    with col1:
        if st.button("Shutdown"):
            subprocess.run(["sudo", "poweroff"])

st.divider()

# Prints instructions for navigation
st.write("Use the menu on the left to navigate between pages.")

