import requests
import re
from colorama import Fore, Style
from datetime import datetime
def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not re.match(regex, url):
        return False
    return True

def check_server(url, pdf):
    HTML = ""
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la requête : ", e)
        return f"Erreur lors de la requête : {e}"

    server = response.headers.get("Server")
    x_powered_by = response.headers.get("X-Powered-By")

    if server is not None:
        print(f">>> {Fore.GREEN}[+] Webserver is  : {server}{Style.RESET_ALL}")
        HTML += f"<p>Web server : {server}<p>"
    if x_powered_by is not None:
        print(f">>> {Fore.GREEN}[+] Webserver uses :  {x_powered_by}{Style.RESET_ALL}")
        HTML += f"<p>Server uses : {x_powered_by}</p>"

    if "Content-Encoding" in response.headers:
        print(f">>> {Fore.YELLOW}[-] The server supports compression.{Style.RESET_ALL}")
        HTML += f"<p>The server supports compression.</p>"
    else:
        print(f">>> {Fore.YELLOW}[-] The server doesn't support compression.{Style.RESET_ALL}")
        HTML += f"<p>The server doesn't support compression.</p>"

    version_regex = re.compile(r"\d+\.\d+(\.\d+)?")
    for header in response.headers:
        match = version_regex.search(response.headers[header])
        if match:
            print(f">>> {Fore.GREEN}[+] Version of software might be found in the following header '{header}' : {match.group(0)} {Style.RESET_ALL}")
            HTML += f"<p>Version of software might be found in the following header {header} : {match.group(0)}</p>"

    if response.status_code in [301, 302]:
        loca_header = response.headers.get("Location")
        print(f">>> [+] Target URL uses redirection towards : {loca_header}")
        HTML += f"<p>Target URL uses redirection towards {loca_header}</p>"
    else:
        print(f">>> {Fore.YELLOW}[-] Target URL don't use any redirection{Style.RESET_ALL}")
        HTML += f"<p>Target URL don't use any redirection</p>"

    if response.status_code == 401:
        print(">>> [+] Target URL is protected by a basic HTTP authentication")
        HTML += f"<p>Target URL is protected by a basic HTTP authentication</p>"
    else:
        print(f">>> {Fore.YELLOW}[-] Target URL isn't protected by a basic HTTP authentication{Style.RESET_ALL}")
        HTML += f"<p>Target URL isn't protected by a basic HTTP authentication</p>"

    headers = {
        "X-Frame-Options": "",
        "X-XSS-Protection": "",
        "X-Content-Type-Options": ""
    }

    try:
        response = requests.get(url, headers=headers)

        if "X-Frame-Options" not in response.headers:
            print(f">>> {Fore.GREEN}[+] The anti-clickjacking X-Frame-Options header is not present.{Style.RESET_ALL}")
            HTML += f"<p>The anti-clickjacking X-Frame-Options header is not present.</p>"
        if "X-XSS-Protection" not in response.headers:
            print(f">>> {Fore.GREEN}[+] The X-XSS-Protection header is not defined.{Style.RESET_ALL}")
            HTML += f"<p>The X-XSS-Protection header is not defined.</p>"
        if "X-Content-Type-Options" not in response.headers:
            print(f">>> {Fore.GREEN}[+] The X-Content-Type-Options header is not set.{Style.RESET_ALL}")
            HTML += f"<p>The X-Content-Type-Options header is not set.</p>"
    except:
        print("Error occurred while sending request to the URL")
        HTML += f"<p>Error occurred while sending request to the URL</p>"

    return HTML

def check_robots_txt(url):
    try:
        r = requests.get(url + "/robots.txt")
        if r.status_code == 200:
            result = f"robots.txt is publicly accessible.\nContent of robots.txt:\n{r.text}"
            print(f">>> {Fore.GREEN}[+] {result}{Style.RESET_ALL}")
            return result
        else:
            result = "robots.txt is not publicly accessible."
            print(f">>> {Fore.YELLOW}[-] {result}{Style.RESET_ALL}")
            return result
    except requests.exceptions.RequestException as e:
        result = f"Exception Occured: {e}"
        print(f">>> [-] {result}")
        return result

def find_github(url):
    try:
        r = requests.get(url + "/.git")
        valid_codes = [200, 204, 301, 302, 307, 401, 403, 407]
        if r.status_code in valid_codes:
            result = "A github repository has been found. Might be vulnerable to gitDumper."
            print(f">>> {Fore.GREEN}[+] {result}{Style.RESET_ALL}")
            return result
        else:
            result = "No github repository found."
            print(f">>> {Fore.RED}[-] {result}{Style.RESET_ALL}")
            return result
    except requests.exceptions.RequestException as e:
        result = f"Exception Occured: {e}"
        print(f">>> [-] {result}")
        return result

def url_discover(url):
    if not is_valid_url(url):
        result = "Error: url format isn't valid"
        print(f">>> {Fore.RED}[-] {result}{Style.RESET_ALL}")
        return result

    if not url.endswith('/'):
        url += '/'
    try:
        response = requests.get(url)
        if response.status_code not in [200, 204, 301, 302, 307, 401, 403, 407]:
            result = f"Error. Url unreachable. Status code: {response.status_code}"
            print(f">>> {Fore.RED}[-] {result}{Style.RESET_ALL}")
            return result
    except requests.exceptions.RequestException as e:
        result = f"Exception Occurred while trying to reach {url}: {e}"
        print(f">>> {Fore.RED}[-] {result}{Style.RESET_ALL}")
        return result

    result = f"Started at {datetime.now()}"
    print(f">>> {Fore.GREEN}[+] {result}{Style.RESET_ALL}")
    return result
