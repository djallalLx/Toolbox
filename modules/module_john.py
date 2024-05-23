import subprocess

def run_john(hash_file_path, format=None):
    john_path = "/usr/sbin/john"
    command = [john_path]
    if format:
        command.extend(["--format=" + format])
    command.append(hash_file_path)

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"John the Ripper a rencontré une erreur : {e.stderr}"

def show_john_results(hash_file_path):
    john_path = "/usr/sbin/john"
    command = [john_path, "--show", hash_file_path]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Erreur lors de l'affichage des résultats : {e.stderr}"
