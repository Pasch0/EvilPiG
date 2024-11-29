import os
import random
import threading
import time
import sys
from scapy.all import RadioTap, Dot11, Dot11Beacon, Dot11Elt, sendp

# Lista de SSIDs engraçados
ssids = [
    "Use Esse, Não O Outro",
    "Linksys Abraham",
    "Benjamin FrankLAN",
    "Martim Router King",
    "Wi-Fi Bonitão",
    "LAN Solo",
    "404 Wi-Fi Inexistente",
    "Carregando...",
    "Esconda Seu Wi-Fi",
    "Van de Vigilância FBI 01",
    "LAN Antes do Tempo",
    "Wi-Ficar ou Não Ficar",
    "Doeu Quando IP",
    "Wi-Fi Art Thou Romeo",
    "Eu Acredito no Wi-Fi",
    "Sem Mais Wi-Fi",
    "Não Sou um Hotspot",
    "Deixe o Hotspot Quente",
    "Saia da Minha LAN",
    "Acesso Negado",
    "Essa LAN é Sua LAN",
    "Não Passa de Senha",
    "RIP Neutralidade de Rede",
    "Sem Acesso à Internet",
    "Eu Sou O Que Pinga",
    "Atenção: Wi-Fi em Progresso",
    "Não É O Wi-Fi Que Você Está Procurando",
    "A Wi-Fi Desperta",
    "A Força Está com Esse Wi-Fi",
    "Wi-Fi, Você é Minha Única Esperança",
    "Roteador? Eu Mal a Conheço",
    "Diga Que Meu Wi-Fi a Ama",
    "Não É Seu Wi-Fi",
    "Procurando Sinal",
    "Vou Trabalhar por Wi-Fi",
    "Wi-Fi Grátis... Só que Não",
    "Go Go Gadget Wi-Fi",
    "Lar Doce Rede",
    "404 Rede Não Encontrada",
    "Não Toque no Meu Wi-Fi",
    "Wi-Fi nas Nuvens",
    "Quem Bate? Wi-Fi",
    "Wi-Fi Finalmente Chegou",
    "Wi-Fi no Telhado",
    "Não Encontrei Wi-Fi",
    "Não Há Lugar Como 192.168.0.1",
    "404 Wi-Fi Não Encontrado",
    "A LAN do Outro Lado",
    "Não Há Wi-Fi Como o Seu",
    "Wi-Fi Bonito de Novo",
    "Mantenha a Calma e Conecte-se ao Wi-Fi",
    "Ctrl+Alt+Del Seu Wi-Fi",
    "Wi-Fi A-Go-Go",
    "Acesso Negado – Tente Novamente",
    "Esse Wi-Fi Agora é Meu",
    "Wi-Fi Espaguete",
    "O Wi-Fi Que Sobreviveu",
    "Seu Wi-Fi Está Fraco",
    "Clube do Wi-Fi",
    "Não é um Hotspot, Passe",
    "A LAN dos Mortos",
    "Rápido e Furioso: Drift do Wi-Fi",
    "Bateria Fraca, Wi-Fi Forte",
    "Roteador, Eu Mal Te Conheço",
    "Wi-Fi Hackeado, Tente Novamente",
    "Tente Novamente Mais Tarde Wi-Fi",
    "Wi-Fi na Selva",
    "Wi-Fi? Mais Como Por Que-Fi",
    "Confissões do Wi-Fi",
    "O Código Wi-Fi",
    "Eu Tenho o Wi-Fi Agora",
    "Wi-Fi Acabou Aqui",
    "Paraíso dos Hackers",
    "Wi-Fi Aberto Está Aberto",
    "Sem Wi-Fi Para Você",
    "Viva La Wi-Fi",
    "Agente Secreto Wi-Fi",
    "Acesso à Internet: Não Encontrado",
    "Wi-Fi ou Nada",
    "Alerta Vermelho: Wi-Fi Caiu",
    "Nenhum Sinal Encontrado",
    "Wi-Fi Distrito 9",
    "Wi-Fi Selvagem",
    "Não Perturbe, Wi-Fi em Manutenção",
    "Wi-Fi da Web Negra",
    "WIFI>VOCÊ",
    "Rede de Casa #1",
    "Internet Grátis – Totalmente Legítima",
    "Pirata Wi-Fi",
    "Missão Impossível Wi-Fi",
    "Banana-Fi",
    "Wi-Fi e Relaxa",
    "A Internet é Meu Docinho",
    "Se Você Pode Ler Isso, Está Muito Perto",
    "Wi-Fi Heisenberg",
    "Olha Mãe, Eu Tenho Wi-Fi",
    "Rede Insegura",
    "A Zona Wi-Fi",
    "Wi-Fi Para Sempre",
    "Por Que Tão Sério? Wi-Fi",
    "Quer Jogar Wi-Fi?",
    "Quem Precisa de Roteador?",
    "Terra do Wi-Fi",
    "Silêncio das LANs",
    "Não Olhe Meu Wi-Fi",
    "Wi-Fi Viral",
    "Wi-Fi e o Furioso",
    "El Wi-Fi Loco",
    "Wi-Fi Ultra Secreto",
    "Mantenha o Wi-Fi, Deixe o Drama",
    "Zona Wi-Fi Proibida",
    "Acesso Permitido: Zona Wi-Fi",
    "Mi-Fi, Nem Pensar",
    "Rede Detectada",
    "Brinque com Seu Wi-Fi",
    "Conecte-se por Sua Conta e Risco",
    "Melhor Wi-Fi de Todos",
    "Você Não Pode Me Pegar Wi-Fi",
    "Mãe, Estou no Wi-Fi",
    "Dial-Up Quem?",
    "WAN É Meu LAN",
    "Os Jogos Wi-Fi",
    "Internet em Chamas",
    "Só LAN Nele",
    "Wifi Subindo, Dude",
    "Onde Está o Wi-Fi?",
    "Traga Seu Próprio Roteador"
]

# Configurações de canal
channels = [1, 6, 11]  # Ajuste conforme necessário
mac_prefix = "02:CA:FF:EE:"  # Prefixo fictício de MAC

def generate_random_mac():
    """Gera um MAC aleatório."""
    return mac_prefix + ":".join(f"{random.randint(0x00, 0xFF):02x}" for _ in range(2))

def generate_beacon(ssid, mac, channel):
    """Gera um pacote beacon frame."""
    dot11 = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=mac, addr3=mac)
    beacon = Dot11Beacon(cap="ESS")
    ssid_elt = Dot11Elt(ID="SSID", info=ssid.encode(), len=len(ssid))
    rates_elt = Dot11Elt(ID="Rates", info=b"\x82\x84\x8b\x96")
    dsset_elt = Dot11Elt(ID="DSset", info=bytes([channel]))
    packet = RadioTap() / dot11 / beacon / ssid_elt / rates_elt / dsset_elt
    return packet

def send_beacons_for_ssid(ssid, iface):
    """Envia pacotes de beacon frame para um SSID específico."""
    while True:
        try:
            mac = generate_random_mac()
            channel = random.choice(channels)
            packet = generate_beacon(ssid, mac, channel)
            sendp(packet, iface=iface, count=32000, inter=0.5, verbose=False)
        except Exception as e:
            print(f"Erro ao enviar beacon para {ssid}: {e}")
            continue  # Continua enviando beacons para outros SSIDs

def switch_channel(iface):
    """Troca canais periodicamente."""
    while True:
        for channel in channels:
            try:
                os.system(f"iwconfig {iface} channel {channel}")
                time.sleep(1)
            except Exception as e:
                print(f"Erro ao trocar canal: {e}")
                continue

def main(iface):
    """Função principal que executa o script."""
    try:
        print("Iniciando spam de beacons...")

        # Checa se o modo monitor está ativo
        if os.system(f"iwconfig {iface}") != 0:
            print(f"Interface {iface} não encontrada ou não está no modo monitor.")
            exit(1)

        # Inicia a thread para trocar de canal
        channel_thread = threading.Thread(target=switch_channel, args=(iface,), daemon=True)
        channel_thread.start()

        # Inicia as threads para cada SSID
        ssid_threads = []
        for ssid in ssids:
            thread = threading.Thread(target=send_beacons_for_ssid, args=(ssid, iface), daemon=True)
            ssid_threads.append(thread)
            thread.start()

        # Mantém o script ativo até receber uma interrupção
        while True:
            time.sleep(1)  # Aguardar para não interromper o loop principal

    except KeyboardInterrupt:
        print("\nEncerrando o script...")
        sys.exit(0)  # Encerra o script ao pressionar Ctrl+C
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}. Reiniciando...")
        time.sleep(2)
        main(iface)  # Reinicia o script em caso de erro

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <interface>")
        sys.exit(1)

    interface_name = sys.argv[1]
    main(interface_name)