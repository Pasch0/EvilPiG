import os
from time import sleep
import sys

def start_tmux_session(interface, caplet):
    # Start a new tmux session named 'wifi-scan-novo'
    os.system(f'tmux new-session -d -s wifi-scan-novo')

    # List of commands to execute in the tmux session
    command = f'bettercap -iface {interface} -caplet {caplet}'

    os.system(f'airmon-ng stop {interface}')
    sleep(0.5)
    os.system(f'airmon-ng start {interface}')
    sleep(0.5)
    os.system(f'tmux send-keys -t wifi-scan-novo "{command}" C-m')
    sleep(0.5)

    # Wait for 25 seconds before killing the tmux session
    sleep(30)
    os.system('tmux kill-session -t wifi-scan-novo')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python script.py <interface> <caplet>")
        sys.exit(1)

    interface = sys.argv[1]
    caplet = sys.argv[2]
    
    try:
        count = 0
        while True:
            start_tmux_session(interface, caplet)
            count += 1
            if count >= 5:
                sleep(3)
            else:
                sleep(30)
    except KeyboardInterrupt:
        print("Encerrando o script...")
        sys.exit(0)