import subprocess
import ipaddress
import datetime
import os
from jinja2 import Environment, FileSystemLoader 
from datetime import datetime 
from colorama import Fore, Style
import time
from colorama import Fore, Style
import re 
from modules.module_hydra import run_hydra as main_hydra
from modules.module_hydra import print_hydra_welcome
from modules.module_hydra import start_animation, stop_animation

from logger import log_action

def run_nmap(target):
    log_action("Nmap", f"Scanned target {target}")
    # Existing code for running nmap

def print_nmap_logo():
    log_action("Nmap", "Printed Nmap logo")
    # Existing code for printing the nmap logo

def validate_ip(ip):
    log_action("Nmap", f"Validated IP {ip}")
    # Existing code for validating IP



def print_nmap_logo():
    logo_lines = [
        "                    ___.-------.___",
        "                _.-' ___.--;--.___ `-._",
        "             .-' _.-'  /  .+.  \  `-._ `-.",
        "           .' .-'      |-|-o-|-|      `-. `.",
        "          (_ <O__      \\  `+'  /      __O> _)",
        "            `--._``-..__`._|_.'__..-''_.--'",
        "                  ``--._________.--''",
        "   ____  _____  ____    ____       _       _______",
        "  |_   \\|_   _||_   \\  /   _|     / \\     |_   __ \\",
        "    |   \\ | |    |   \\/   |      / _ \\      | |__) |",
        "    | |\\ \\| |    | |\\  /| |     / ___ \\     |  ___/",
        "   _| |_\\   |_  _| |_\\/_| |_  _/ /   \\ \\_  _| |_",
        "  |_____\\____||_____||______||____| |____||_____|",
    ]

    print(Fore.RED + Style.BRIGHT)
    for line in logo_lines:
        print(line)
        time.sleep(0.1)  # Delays for 0.1 seconds between each line
    print(Style.RESET_ALL)

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def run_nmap(target, option):
    nmap_options = {
        1: "-sS ",
        2: "-sU  ",
        3: "-O  ",
        4: "-sV  ",
        5: "-A  "
    }
    if option in nmap_options:
        command = f"nmap {nmap_options[option]} {target}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        # Enregistrer la sortie de Nmap dans une variable
        nmap_output = output.decode('utf-8')

        # Afficher la sortie de Nmap
        print(nmap_output)

        port_22_open = re.search(r"22\/tcp\s+open", nmap_output)

        if port_22_open:
            print(f"\nLe port 22 (SSH) est ouvert sur la cible {target}. Voulez-vous :")
            print(f"{Fore.GREEN}1. Cracker le SSH avec Hydra{Style.RESET_ALL}")
            print(f"{Fore.GREEN}2. Effectuer un autre scan Nmap{Style.RESET_ALL}")
            print(f"{Fore.GREEN}3. Retourner au menu principal{Style.RESET_ALL}")

            choice = input("Entrez votre choix : ")

            if choice == '1':
                print_hydra_welcome()
                animation_thread = start_animation()
                result = main_hydra(target, "u.txt", "p.txt", 22, "ssh")
                stop_animation(animation_thread)

                # Sortie de Hydra
                hydra_output = ""

                # Trouver la ligne contenant "login:" et "password:"
                for line in result.split('\n'):
                    if "login:" in line and "password:" in line:
                        # Colorier "login: gnulinux" et "password: Mounasolui" en vert
                        colored_line = line.replace("login:", "\033[92mlogin: gnulinux\033[0m")
                        colored_line = colored_line.replace("password:", "\033[92mpassword:\033[0m")
                        hydra_output += colored_line + "\n"
                        break
                # Afficher la sortie de Hydra en vert
                print("\033[92m" + hydra_output + "\033[0m")

                print("\nHydra terminé. Résultat :")

                # Vider la variable pour éviter que la sortie de Nmap ne soit affichée à nouveau
                nmap_output = ""

            elif choice == '2':
                from menu import main_nmap
                main_nmap()
            elif choice == '3':
                from menu import main_menu
                main_menu()
            else:
                print(f"{Fore.RED}Choix non valide. Veuillez essayer à nouveau.{Style.RESET_ALL}")

        return None, nmap_output
    else:
        return "Option non valide. Veuillez choisir une option valide.", None
