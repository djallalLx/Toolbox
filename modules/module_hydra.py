import subprocess
import os
from colorama import Fore, Style
import time
import threading 
import socket
def print_hydra_welcome():
    logo_lines = [
        "                  ⠄⠄⣴⣶⣤⡤⠦⣤⣀⣤⠆⠄⠄⠄⠄⠄⣈⣭⣭⣿⣶⣿⣦⣼⣆⠄⠄⠄⠄⠄⠄⠄⠄",
        "                  ⠄⠄⠄⠉⠻⢿⣿⠿⣿⣿⣶⣦⠤⠄⡠⢾⣿⣿⡿⠋⠉⠉⠻⣿⣿⡛⣦⠄⠄⠄⠄⠄⠄",
        "                  ⠄⠄⠄⠄⠄⠈⠄⠄⠄⠈⢿⣿⣟⠦⠄⣾⣿⣿⣷⠄⠄⠄⠄⠻⠿⢿⣿⣧⣄⠄⠄⠄⠄",
        "                  ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣸⣿⣿⢧⠄⢻⠻⣿⣿⣷⣄⣀⠄⠢⣀⡀⠈⠙⠿⠄⠄⠄⠄",
        "                  ⠄⠄⢀⠄⠄⠄⠄⠄⠄⢠⣿⣿⣿⠈⠄⠄⠡⠌⣻⣿⣿⣿⣿⣿⣿⣿⣛⣳⣤⣀⣀⠄⠄",
        "                  ⠄⠄⢠⣧⣶⣥⡤⢄⠄⣸⣿⣿⠘⠄⠄⢀⣴⣿⣿⡿⠛⣿⣿⣧⠈⢿⠿⠟⠛⠻⠿⠄⠄",
        "                  ⠄⣰⣿⣿⠛⠻⣿⣿⡦⢹⣿⣷⠄⠄⠄⢊⣿⣿⡏⠄⠄⢸⣿⣿⡇⠄⢀⣠⣄⣾⠄⠄⠄",
        "                  ⣠⣿⠿⠛⠄⢀⣿⣿⣷⠘⢿⣿⣦⡀⠄⢸⢿⣿⣿⣄⠄⣸⣿⣿⡇⣪⣿⡿⠿⣿⣷⡄⠄",
        "                  ⠙⠃⠄⠄⠄⣼⣿⡟⠌⠄⠈⠻⣿⣿⣦⣌⡇⠻⣿⣿⣷⣿⣿⣿⠐⣿⣿⡇⠄⠛⠻⢷⣄",
        "                  ⠄⠄⠄⠄⠄⢻⣿⣿⣄⠄⠄⠄⠈⠻⣿⣿⣿⣷⣿⣿⣿⣿⣿⡟⠄⠫⢿⣿⡆⠄⠄⠄⠁",
        "                  ⠄⠄⠄⠄⠄⠄⠻⣿⣿⣿⣿⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⡟⢀⣀⣤⣾⡿⠃⠄⠄⠄⠄",
        "                  ⠄⠄⠄⠄⢰⣶⠄⠄⣶⠄⢶⣆⢀⣶⠂⣶⡶⠶⣦⡄⢰⣶⠶⢶⣦⠄⠄⣴⣶⠄⠄⠄⠄",
        "                  ⠄⠄⠄⠄⢸⣿⠶⠶⣿⠄⠈⢻⣿⠁⠄⣿⡇⠄⢸⣿⢸⣿⢶⣾⠏⠄⣸⣟⣹⣧⠄⠄⠄",
        "                  ⠄⠄⠄⠄⠸⠿⠄⠄⠿⠄⠄⠸⠿⠄⠄⠿⠷⠶⠿⠃⠸⠿⠄⠙⠷⠤⠿⠉⠉⠿⠆⠄⠄"
    ]

    print(Fore.RED + Style.BRIGHT)
    for line in logo_lines:
        print(line)
        time.sleep(0.1)  # Delays for 0.1 seconds between each line to create a progressive display effect
    print(Style.RESET_ALL)
    print(f"{Fore.RED}Bienvenue sur Hydra{Style.RESET_ALL}")


def run_hydra(target, userlist_path, wordlist_path, port, service):
    # Construction de la commande Hydra
    command = [
        "hydra",
        "-L", userlist_path,  # Utilise un fichier pour les noms d'utilisateur
        "-P", wordlist_path,  # Utilise un fichier pour les mots de passe
        "-s", str(port),  # Spécifie le port si nécessaire, utile pour des services non standards
        "-t", "4",
        "-I",
        service + "://" + target  # Spécifie le service et la cible
    ]

    try:
        # Exécution de la commande Hydra
        result = subprocess.run(command, text=True, capture_output=True, check=True)
        print("Hydra a démarré avec succès. Voici la sortie :")
        print(result.stdout)  # Affiche la sortie standard
        if result.stderr:
            print("Erreur de sortie standard :")
            print(result.stderr)  # Affiche les erreurs si présentes
    except subprocess.CalledProcessError as e:
        # Affiche la sortie d'erreur si Hydra échoue
        print(f"Erreur lors de l'exécution de Hydra: {e.stderr}")
    except Exception as e:
        print(f"Erreur inattendue: {str(e)}")

    return result.stdout if result.stdout else "Aucune sortie significative de Hydra."
# Variable globale pour contrôler l'état de l'animation
animation_running = False

def animate():
    symbols = ["💀", "🕵️‍♂️", "💀", "🕵️‍♂️"]
    idx = 0
    while animation_running:
        print("\rDémarrage de Hydra... " + symbols[idx % len(symbols)], end="")
        idx += 1
        time.sleep(0.5)  # Ajustement de la vitesse de l'animation

def start_animation():
    global animation_running
    animation_running = True
    thread = threading.Thread(target=animate)
    thread.start()
    return thread

def stop_animation(thread):
    global animation_running
    animation_running = False
    thread.join()

# Exemple d'utilisation de la fonction
# run_hydra("192.168.2.6", "usernames.txt", "rockyou.txt", 22, "ssh")
