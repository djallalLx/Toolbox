import requests
import json
import subprocess
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Ajout de la fonction pour imprimer le logo DNS
def print_dns_logo():
    logo = """
     ###                      ###                       ###
     ##                       ##                        ##
     ##   #####     #####     ##      ####     ####     ##  ##  ##  ##   ######
  #####   ##  ##   ##         ##     ##  ##   ##  ##    ## ##   ##  ##    ##  ##
 ##  ##   ##  ##    #####     ##     ##  ##   ##  ##    ####    ##  ##    ##  ##
 ##  ##   ##  ##        ##    ##     ##  ##   ##  ##    ## ##   ##  ##    #####
  ######  ##  ##   ######    ####     ####     ####     ##  ##   ######   ##
                                                                         ####
    """
    print(logo)

def DNSLookUp(domain, htmlRender=False):
    print_dns_logo()  # Appeler la fonction pour afficher le logo
    URL = "https://networkcalc.com/api/dns/lookup/" + domain
    response = requests.get(URL)
    displayInfos = ""

    if htmlRender:
        spacing = "<br>"  # Pour le rendu HTML
    else:
        spacing = "\n"

    if response.status_code != 200:
        return f"{spacing}Erreur lors de la récupération des informations DNS. Veuillez vérifier votre domaine ou l'API.{spacing}"

    data = response.json()
    if data['status'] != 'OK':
        error_message = "Pas de message d'erreur spécifique."
        return f"{spacing}Erreur avec l'API : {data.get('message', error_message)}{spacing}"

    displayInfos += f"{spacing}========================================{spacing}"
    displayInfos += f"DNS Informations about {data['hostname']}{spacing}"
    displayInfos += f"=========================================={spacing}"

    records = data['records']

    for record_type in ['A', 'CNAME', 'MX', 'NS', 'SOA', 'TXT']:
        record_data = records.get(record_type)
        if record_data:
            if htmlRender:
                displayInfos += f"| {record_type} | {record_data}{spacing}"
            else:
                displayInfos += f"{record_type} : {record_data}\n"
        else:
            if htmlRender:
                displayInfos += f"| {record_type} | No record found{spacing}"
            else:
                displayInfos += f"{record_type} : No record found\n"

    return displayInfos

def fetch_dns_records_dig(domain):
    print_dns_logo()  # Appeler la fonction pour afficher le logo
    command = ["dig", "+noall", "+answer", domain, "ANY"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if result.stdout:
            return result.stdout
        else:
            return "Aucun enregistrement trouvé ou erreur dans l'exécution de dig."
    except subprocess.CalledProcessError:
        return "Erreur lors de l'exécution de la commande dig."

