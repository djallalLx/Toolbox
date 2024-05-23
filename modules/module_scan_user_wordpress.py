import urllib.request
import urllib.parse
import sys
from colorama import Fore, Style
from urllib.parse import urlparse
import random


def print_wordpress_logo():
    logo = f"""{Fore.LIGHTBLUE_EX}
                  `-/+osssssssssssso+/-`
               ./oys+:.`            `.:+syo/.
            .+ys:.   .:/osyyhhhhyyso/:.   ./sy+.
          /ys:   -+ydmmmmmmmmmmmmmmmmmmdy+-   :sy/
        /h+`  -odmmmmmmmmmmmmmmmmmmmmmmmmmmdo-  `+h/
      :ho`  /hmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmds/   `oh:
    `sy.  /hmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmd+        .ys`
   .ho  `sdddhhhyhmmmdyyhhhdddddhhhyydmmmmy           oh.
  .h+          ``-dmmy.``         ``.ymmmmh            +h.
 `ho  `       /mmmmmmmmmmo       .dmmmmmmmms        ~~  oh`
 oy  .h`       ymmmmmmmmmm:       /mmmmmmmmmy`      -d.  yo
.d-  ymy       `dmmmmmmmmmd.       ymmmmmmmmmh`     /my  -d.
oy  -mmm+       /mmmmmmmmmmy       .dmmmmmmmmmy     ymm-  yo
h+  +mmmd-       smmmmmmmmmm+       /mmmmmmmmmm-   :mmm+  +h
d/  smmmmh`      `dmmmmmmmmmd`       smmmmmmmmm:  `dmmms  /d
d/  smmmmms       :mmmmmmmmm+        `dmmmmmmmd.  smmmms  /d
h+  +mmmmmm/       smmmmmmmh  +       /mmmmmmmy  /mmmmm+  +h
oy  -mmmmmmd.      `dmmmmmd- +m/       smmmmmd. .dmmmmm-  yo
.d-  ymmmmmmh       :mmmmm+ .dmd-      `dmmmm/  ymmmmmy  -d.
 oy  .dmmmmmmo       smmmh  hmmmh`      :mmmy  +mmmmmd.  yo
 `ho  -dmmmmmd:      `dmd- ommmmms       smd- .dmmmmd-  oh`
  .h+  -dmmmmmd`      :m+ -dmmmmmm:      `do  hmmmmd-  +h.
   .ho  .ymmmmmy       + `hmmmmmmmd.      :` ommmmy.  oh.
    `sy.  /hmmmm+        ommmmmmmmmy        -dmmh/  .ys`
      :ho`  /hmmd-      :mmmmmmmmmmmo      `hmh/  `oh:
        /h+`  -odh`    `dmmmmmmmmmmmd:     oo-  `+h/
          /ys:   ~~    smmmmmmmmmmmmmd`       :sy/
            .+ys/.    `/osyyhhhhyyso/:`   ./sy+.
               ./oys+:.`            `.:+syo/.
                   `-/+osssssssssssso+/-`
{Style.RESET_ALL}"""
    print(logo)

def uniq(lst):
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item

def sort_and_deduplicate(l):
    return list(uniq(sorted(l, reverse=False)))

def curllib(req, params=None, postdata=None):
    headers = {
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        req = urllib.request.Request(req, postdata, headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read()
    except Exception as e:
        return False

def sout(s):
    sys.stdout.write(s + "\r")
    sys.stdout.flush()

def finder(text, start, end, index=1):
    try:
        text = text.split(start)[index]
        return text.split(end)[0]
    except:
        return ""

def find_username(html=None):
    if html is not None:
        return {
            "user": finder(html, '/author/', '/'),
            "name": finder(html, '<title>', '</title>').split(',')[0]
        }

def scan_wordpress_users(site, usern):
    results = []
    max_login_len = max_name_len = 0
    site = urlparse(site)

    if site:
        site = site.scheme + "://" + site.netloc + "/" if site.path == "" else site.scheme + "://" + site.netloc + site.path
    else:
        return "[#]: Wrong SITE format (example: http://target.com/)"

    print_wordpress_logo()

    for x in range(0, usern):
        sout("[+]: %" + str(100 / usern * x) + "\t")
        try:
            tmp = curllib(site, '', urllib.parse.urlencode({"author": (x + 1)}).encode('utf-8'))
            if tmp == False:
                pass
            tmp = find_username(tmp.decode('utf-8'))
        except:
            pass
        if isinstance(tmp, dict) and len(tmp['user']):
            results.append(tmp)
            max_login_len = len(tmp['user']) if max_login_len < len(tmp['user']) else max_login_len
            max_name_len = len(tmp['name']) if max_name_len < len(tmp['name']) else max_name_len

    if not results:
        error_messages = [
            "Le site utilise WordPress, mais les pages d'auteur sont désactivées ou masquées.",
            "Le site utilise des mesures de sécurité pour empêcher l'énumération des utilisateurs.",
            
        ]
        error_message = random.choice(error_messages)
        return error_message

    results = sort_and_deduplicate(results)
    output = f"Found {len(results)} users in {site}\n"

    login_space = (max_login_len - len("Login") + 1) * " "
    name_space = (max_name_len - len("Name") + 1) * " "
    login_bar = ((max_login_len - len("Login") + 1) + 6) * "-"
    name_bar = ((max_name_len - len("Name") + 1) + 5) * "-"
    header = "| Id | Login" + login_space + "| Name" + name_space + "|"

    output += f"  +----+{login_bar}+{name_bar}+\n"
    output += f"  {header}\n"
    output += f"  +----+{login_bar}+{name_bar}+\n"

    for x in range(0, len(results)):
        id_space = (3 - len(str(x + 1))) * " "
        login_space = (max_login_len - len(results[x]['user']) + 1) * " "
        name_space = (max_name_len - len(results[x]['name']) + 1) * " "
        output += f"  | {str(x + 1)}{id_space}| {results[x]['user']}{login_space}| {results[x]['name']}{name_space}|\n"

    output += f"  +----+{login_bar}+{name_bar}+\n"


    return output
