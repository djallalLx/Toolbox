TOOLBOX AUTOMATISE 
  ___         _          _      
 | _ \\___ _ _| |_ ___ __| |_    
 |  _/ -_) ' \\  _/ -_|_-<  _|   
 |_|_\\___|_||_\\__\\___/__\\__|   
 |_   _|__  ___| | |__  _____ __
   | |/ _ \\/ _ \\ | '_ \\/ _ \\ \\ /
   |_|\___/\___/_|_.__/\___/_\_\

## INTRODUCTION ## 
La Toolbox est un outil de sécurité complet destiné à l'énumération, la recherche de vulnérabilités, le craquage de mots de passe, l'inspection web, et plus encore. Ce script Python vous permet d'accéder à divers modules de sécurité pour effectuer différentes tâches d'audit et de test. 

gitclone https://github.com/djallalLx/ToolboxV1.git

## Prérequis ##
Avant d'exécuter la Toolbox, assurez-vous d'avoir installé les dépendances nécessaires. 

chmod +x setup.sh 
./setup.sh 
pip3 install requirements.txt 

## UTILISATION ##
python3 menu.py 

## Menu principale ## 

À l'exécution du script, vous verrez un menu principal avec les options suivantes :

Énumération
Recherche CVE
Craquage de mot de passe avec Hydra
Craquage de mot de passe avec John the Ripper
Inspection Web
Scan des utilisateurs WordPress
Injection SQL
Test XSS
Attaque DDoS
Quitter

## Modules ## 

1. Énumération
Ce module propose trois sous-options pour l'énumération :

Nmap : Lancer un scan Nmap sur une cible.
Recherche DNS : Effectuer une recherche DNS basique.
Recherche DNS avancée (dig) : Utiliser dig pour récupérer les enregistrements DNS.
2. Recherche CVE
Rechercher des vulnérabilités connues en utilisant un fichier JSON contenant les informations CVE.

3. Craquage de mot de passe avec Hydra
Utiliser Hydra pour effectuer des attaques de force brute sur divers services (ssh, ftp, etc.).

4. Craquage de mot de passe avec John the Ripper
Utiliser John the Ripper pour craquer des mots de passe à partir de fichiers de hash.

5. Inspection Web
Inspecter une URL pour des informations telles que les en-têtes de serveur, les fichiers robots.txt, la présence de référentiels GitHub, etc.

6. Scan des utilisateurs WordPress
Énumérer les utilisateurs d'un site WordPress pour détecter d'éventuelles vulnérabilités.

7. Injection SQL
Tester une URL pour des vulnérabilités d'injection SQL.

8. Test XSS
Tester une URL pour des vulnérabilités XSS en utilisant un fichier de payloads.

9. Attaque DDoS
Lancer une attaque DDoS sur une cible spécifique. Utiliser uniquement pour des tests autorisés et éthiques.

Quitter
Choisissez cette option pour quitter la Toolbox.

Génération de rapport
Après avoir effectué vos tests, vous pouvez générer un rapport complet des activités en appelant la fonction generate_report.

## AVERTISSEMENT !! ## 
Ce script doit être utilisé uniquement à des fins légales et éthiques. Assurez-vous d'avoir l'autorisation nécessaire avant de lancer des tests de sécurité sur une cible.

## Auteur ##
Toolbox version 1.0 par Djallal

## Contact ##
Pour toute question ou support, veuillez contacter [linx.jaldsad@gmail.com].