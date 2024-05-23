import json
from colorama import Fore, Style

# modules/module_cve_lookup.py
from logger import log_action

def CVELookUp(cve_id):
    log_action("CVE Lookup", f"Looked up CVE ID {cve_id}")
    # Existing code for CVE lookup

def print_cve_logo():
    log_action("CVE Lookup", "Printed CVE logo")
    # Existing code for printing the CVE logo


def print_cve_logo():
    logo = f"""{Fore.BLUE}
  ####    ##  ##    ####
 ##  ##   ##  ##   ##  ##
 ##       ##  ##   ######
 ##  ##    ####    ##
  ####      ##      #####
{Style.RESET_ALL}
"""
    print(logo)
class CVELookUp:
    def __init__(self, file_path):
        self.file_path = file_path  

    def load_data(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def lookup_cve(self, cve_id):
        data = self.load_data()
        for cve in data:
            if cve['CVE'] == cve_id:
                description = cve['Summary']
                cvss_score = cve.get('Max CVSS Base Score', "N/A")
                return f"{Fore.GREEN}Description: {description}\nCVSS Score: {cvss_score}{Style.RESET_ALL}"
        return f"{Fore.RED}Aucune information trouvée pour le CVE {cve_id}.{Style.RESET_ALL}"

