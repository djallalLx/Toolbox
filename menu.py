#!/usr/bin/env python3
import sys
import datetime
import threading
import queue
import os
from colorama import Fore, Style

from modules.module_nmap import run_nmap, print_nmap_logo, validate_ip
from modules.module_dnslookup import DNSLookUp, fetch_dns_records_dig
from modules.module_cve_lookup import CVELookUp, print_cve_logo
from modules.module_hydra import run_hydra, print_hydra_welcome, start_animation, stop_animation
from modules.module_john import run_john, show_john_results
from modules.module_web_inspector import check_server, check_robots_txt, find_github, url_discover, is_valid_url
from modules.module_scan_user_wordpress import scan_wordpress_users, print_wordpress_logo 
from modules.module_sqlinjection import sql_injection_test, print_sqlinjection_logo
from modules.module_xss import run_xss_test, print_xss_logo
from modules.module_ddos import run_ddos_attack
from generate_report import generate_report

def display_header():
    """Affiche l'en-tête du programme."""
    display_info = f"""{Fore.RED}
  ___         _          _      
 | _ \\___ _ _| |_ ___ __| |_    
 |  _/ -_) ' \\  _/ -_|_-<  _|   
 |_|_\\___|_||_\\__\\___/__\\__|   
 |_   _|__  ___| | |__  _____ __
   | |/ _ \\/ _ \\ | '_ \\/ _ \\ \\ /
   |_|\___/\___/_|_.__/\___/_\_\

{Style.RESET_ALL}{Fore.CYAN}
 version 1.0 by Djallal{Style.RESET_ALL}
"""
    print(display_info)

def main_menu():
    """Affiche le menu principal et gère les choix de l'utilisateur."""
    while True:
        display_header()
        print("Bienvenue dans la Toolbox. Veuillez choisir un module :")
        print(f"{Fore.GREEN}1. Énumération{Style.RESET_ALL}")
        print(f"{Fore.GREEN}2. Recherche CVE{Style.RESET_ALL}")
        print(f"{Fore.GREEN}3. Craquage de mot de passe avec Hydra{Style.RESET_ALL}")
        print(f"{Fore.GREEN}4. Craquage de mot de passe avec John the Ripper{Style.RESET_ALL}")
        print(f"{Fore.GREEN}5. Inspection Web{Style.RESET_ALL}")
        print(f"{Fore.GREEN}6. Scan des utilisateurs WordPress{Style.RESET_ALL}") 
        print(f"{Fore.GREEN}7. Injection SQL{Style.RESET_ALL}")
        print(f"{Fore.GREEN}8. Test XSS{Style.RESET_ALL}")
        print(f"{Fore.GREEN}9. Attaque DDoS{Style.RESET_ALL}")
        print(f"{Fore.GREEN}10. Quitter{Style.RESET_ALL}")
        choix = input("Entrez votre choix : ")

        if choix == '1':
            enumeration_menu()
        elif choix == '2':
            main_cve_lookup()
        elif choix == '3':
            main_hydra()
        elif choix == '4':
            main_john()
        elif choix == '5':
            main_web_inspector()
        elif choix == '6':
            main_scan_wordpress_users()  
        elif choix == '7':
            main_sql_injection()
        elif choix == '8':
            main_xss() 
        elif choix == '9':
            run_ddos_attack()
        elif choix == '10':
            print("Merci d'avoir utilisé la Toolbox. À bientôt !")
            sys.exit(0)
        else:
            print(f"{Fore.RED}Choix non valide. Veuillez essayer à nouveau.{Style.RESET_ALL}")

def enumeration_menu():
    """Affiche le menu d'énumération et gère les choix de l'utilisateur."""
    while True:
        print("\nOptions d'Énumération :")
        print(f"{Fore.GREEN}1. Nmap{Style.RESET_ALL}")
        print(f"{Fore.GREEN}2. Recherche DNS{Style.RESET_ALL}")
        print(f"{Fore.GREEN}3. Recherche DNS avancée (dig){Style.RESET_ALL}")
        print(f"{Fore.GREEN}4. Retour{Style.RESET_ALL}")
        choix = input("Entrez votre choix : ")

        if choix == '1':
            main_nmap()
        elif choix == '2':
            main_dns_lookup()
        elif choix == '3':
            main_dns_lookup_advanced()
        elif choix == '4':
            return
        else:
            print(f"{Fore.RED}Choix non valide. Veuillez essayer à nouveau.{Style.RESET_ALL}")

def main_nmap():
    """Gère le module Nmap."""
    print_nmap_logo()

    while True:
        cible = input("Entrez l'adresse IP ou l'URL cible pour l'analyse Nmap : ")
        if not validate_ip(cible):
            print("Adresse IP non valide, veuillez entrer une adresse IP valide.")
        else:
            break

    options = {
        1: "Scan de port TCP (syn)",
        2: "Scan de port UDP",
        3: "Scan OS et version",
        4: "Scan de version (service)",
        5: "Scan agressif"
    }
    while True:
        print("\nChoisissez l'option de scan Nmap en entrant le numéro correspondant :")
        for k, v in options.items():
            print(f"{k}. {v}")

        try:
            option = int(input())
            if option not in options:
                raise ValueError
            break
        except ValueError:
            print("Option non valide. Veuillez choisir une option valide.")

    maintenant = datetime.datetime.now()
    print(f"Lancement de Nmap à {maintenant.strftime('%Y-%m-%d %H:%M:%S')}")
    erreur, resultat = run_nmap(cible, option)
    if erreur:
        print(erreur)
    else:
        print(resultat)

    while True:
        response = input("\nVoulez-vous effectuer une autre analyse Nmap ? (oui/non) : ").lower()
        if response == 'oui':
            return main_nmap()
        elif response == 'non':
            break
        else:
            print("Réponse non valide. Veuillez entrer 'oui' ou 'non'.")

def main_dns_lookup():
    """Gère la recherche DNS basique."""
    domaine = input("Entrez le nom de domaine à rechercher : ")
    resultat = DNSLookUp(domaine)
    print(resultat)

def main_dns_lookup_advanced():
    """Gère la recherche DNS avancée avec dig."""
    domaine = input("Entrez le nom de domaine pour la recherche avancée avec dig : ")
    print("Récupération des enregistrements DNS avec dig...")
    result = fetch_dns_records_dig(domaine)
    print(result)

def main_cve_lookup():
    """Gère le module de recherche CVE."""
    print_cve_logo()
    print("Module de Recherche CVE")
    cve_lookup = CVELookUp("cve.json")  

    while True:
        cve_id = input("Entrez l'ID CVE à rechercher (e.g., CVE-2021-34527): ")
        result = cve_lookup.lookup_cve(cve_id)
        print(result)

        another_search = input("Voulez-vous effectuer une autre recherche CVE ? (oui/non): ").strip().lower()
        if another_search != 'oui':
            break


        another_search = input("Voulez-vous effectuer une autre recherche CVE ? (oui/non): ").strip().lower()
        if another_search != 'oui':
            break

def main_hydra():
    """Gère le module Hydra pour le craquage de mot de passe."""
    print_hydra_welcome()

    target = input("Entrez l'adresse IP de la cible : ")
    userlist_path = input("Entrez le chemin vers la liste des utilisateurs : ")
    wordlist_path = input("Entrez le chemin vers la liste de mots de passe : ")
    port = int(input("Entrez le port sur lequel le service est exécuté : "))
    service = input("Entrez le service (ssh, ftp, etc.) : ")

    animation_thread = start_animation()

    result = run_hydra(target, userlist_path, wordlist_path, port, service)

    stop_animation(animation_thread)

    result_lines = result.split('\n')
    for line in result_lines:
        if "login:" in line or "password:" in line:
            line = line.replace("login:", f"{Fore.GREEN}login:{Style.RESET_ALL}")
            line = line.replace("password:", f"{Fore.GREEN}password:{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{line}{Style.RESET_ALL}")
        else:
            print(line)

    print("\nHydra terminé. Résultat :")

def main_john():
    """Gère le module John the Ripper pour le craquage de mot de passe."""
    print("\nBienvenue dans le module John the Ripper")
    hash_file_path = input("Entrez le chemin du fichier de hash : ")
    format = input("Entrez le format du hash (appuyez sur Entrée si inconnu) : ").strip() or None

    print("\nCracking des hashes en cours...")
    cracking_result = run_john(hash_file_path, format)
    print(cracking_result)

    if input("\nVoulez-vous afficher les résultats du cracking ? (oui/non): ").strip().lower() == 'oui':
        results = show_john_results(hash_file_path)
        print(results)


def main_web_inspector():
    """Gère le module d'inspection web."""
    while True:
        try:
            url = input("Entrez l'URL à inspecter : ").strip()
            if not is_valid_url(url):
                print(">>> [!] L'URL saisie est invalide. Veuillez saisir une URL valide à inspecter.")
                continue

            result_queue = queue.Queue()
            tasks = [
                (check_server, (url, False)),
                (check_robots_txt, (url,)),
                (find_github, (url,)),
                (url_discover, (url,))
            ]

            threads = [threading.Thread(target=lambda f, args: result_queue.put(f(*args)), args=(task[0], task[1])) for task in tasks]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            while not result_queue.empty():
                print(result_queue.get())

            again = input("Voulez-vous inspecter un autre site web ? (oui/non) : ").strip().lower()
            if again != 'oui':
                print("Fin du module d'inspection web.")
                break
        except KeyboardInterrupt:
            print("\nInspection interrompue. Fin du module d'inspection web.")
            break

def main_scan_wordpress_users():
    """Gère le module de scan des utilisateurs WordPress."""
    print_wordpress_logo()

    while True:
        site = input("Entrez l'URL du site WordPress à analyser : ")
        usern = int(input("Entrez le nombre d'utilisateurs à énumérer : "))

        result = scan_wordpress_users(site, usern)
        print(result)

        if result == "Le site utilise des mesures de sécurité pour empêcher l'énumération des utilisateurs.":
            choice = input("Voulez-vous analyser un autre site WordPress ? (o/n) ")
        else:
            choice = input("Voulez-vous analyser un autre site WordPress ? (o/n) ")

        if choice.lower() == "n":
            break

def main_sql_injection():
    print_sqlinjection_logo()
    url = input("Entrez l'URL du site à tester pour l'injection SQL : ")
    param = input("Entrez le nom du paramètre à tester (ex. 'id') : ")
    sql_injection_test(url, param)

def main_xss():
    """Gère le module de test XSS."""
    print_xss_logo()
    url = input("Entrez l'URL à tester pour les vulnérabilités XSS : ")
    param = input("Entrez le nom du paramètre à tester (ex. 'search') : ")
    payload_file = input("Entrez le chemin du fichier de payloads XSS : ")

    print("Test des vulnérabilités XSS en cours...")
    results = run_xss_test(url, param, payload_file)
    
    if results:
        print(f"{Fore.YELLOW}Vulnérabilités XSS trouvées !{Style.RESET_ALL}")
        for payload, target_url in results.items():
            print(f"{Fore.GREEN}Payload: {payload}{Style.RESET_ALL} - URL: {target_url}")
    else:
        print(f"{Fore.RED}Aucune vulnérabilité XSS trouvée.{Style.RESET_ALL}")

def generate_report():
    from generate_report import generate_report
    generate_report()

if __name__ == "__main__":
    main_menu()
