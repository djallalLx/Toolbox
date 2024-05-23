from colorama import Fore, Style
import requests
import urllib.parse

def print_xss_logo():
    print(
        Fore.RED + """
         ##  ##    #####    #####
          ####    ##       ##
           ##      #####    #####
          ####         ##       ##
         ##  ##   ######   ######

        """ + Style.RESET_ALL
    )

def run_xss_test(url, param, payload_file):
    vulnerabilities = {}
    with open(payload_file, "r", encoding='utf-8') as txt:
        payloads = txt.read().splitlines()
        
    total_payloads = len(payloads)
    processed_payloads = 0

    for payload in payloads:
        processed_payloads += 1
        test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
        try:
            response = requests.get(test_url, timeout=5)
            if payload in response.text:
                print(Fore.YELLOW + "Vulnérabilité XSS trouvée" + Style.RESET_ALL)
                print(Fore.YELLOW + f"Payload traité : {payload}" + Style.RESET_ALL)
                print(Fore.YELLOW + f"Lieu de la vulnérabilité : {test_url}" + Style.RESET_ALL)
                print(Fore.YELLOW + "Exploitabilité : La donnée entrée par l'utilisateur est envoyée au site comme du code JavaScript." + Style.RESET_ALL)
                vulnerabilities[payload] = test_url
                break
        except requests.RequestException as e:
            print(f"{Fore.RED}Erreur lors de la requête : {e}{Style.RESET_ALL}")
        
        print(f"{Fore.RED}Aucune vulnérabilité XSS trouvée. {processed_payloads}/{total_payloads} payloads traités.{Style.RESET_ALL}")
    
    if not vulnerabilities:
        print(Fore.RED + "Aucune vulnérabilité XSS trouvée." + Style.RESET_ALL)
    
    return vulnerabilities

if __name__ == "__main__":
    print_xss_logo()
    site_cible = input("Entrez le site cible : ")
    # Vérifie si l'URL est valide
    if urllib.parse.urlparse(site_cible).scheme == '':
        site_cible = 'http://' + site_cible
    site = (site_cible + "/index.php?q=")

    payload_file = input("Entrez le chemin du fichier de payloads XSS : ")

    results = run_xss_test(site, 'q', payload_file)

    if not results:
        print(Fore.RED + "Aucune vulnérabilité XSS trouvée." + Style.RESET_ALL)
    else:
        for payload, url in results.items():
            print(f"{Fore.GREEN}Payload: {payload}{Style.RESET_ALL} - URL: {url}")
