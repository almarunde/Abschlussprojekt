import shutil
import subprocess
import datetime
import tempfile
import os
import logging
from pathlib import Path

# Für Arbeit im Backend und Troubleshooting
# Eventuell zum Ende hin vorerst wieder entfernen
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

logger = logging.getLogger(__name__)

'''
    FUTURE OPT TODOS:
    Zukünftig hybride Lösung VIA pywin32 library von python???

    DIESE HIER WERDEN NOCH DAZUKOMMEN
    - [PROCESS.exe] - KANN ICH DAS ÜBERHAUPT RAUSFINDEN??
            alt notice an Nutzer, dass das ergänzt werden muss
    - [AppDir] - KANN ICH DAS AUSLESEN ????????
    => Vorerst Lösung durch Aufforderung an Nutzer
    
'''

def create_package(msifile, msifilename):
    temp_path = save_temp_file(msifile)

    # Alle wichtigen Daten aus .msi
    regkey = get_regkey(temp_path)
    date = get_date()
    hersteller = get_hersteller(temp_path)
    software = get_software(temp_path)
    version = get_version(temp_path)

    # Aufbau von Ordnerstruktur
    try:
        # Grundstruktur aufbauen
        Path(f"C:/temp/1_msi/{hersteller}/{software}/{version}/Install").mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.info("Fehler bei directory-Erstellung")
        logger.info(e)

    # Vorschrieb kopieren für zu-editierende-inf
    parent_folder =f"C:/temp/1_msi/{hersteller}"
    source_folder = f"{parent_folder}/{software}/{version}"
    install_folder = f"{source_folder}/Install"

    try:
        # Install-Folder befüllen
        shutil.copyfile(".venv/Inf_Sources/Setup.inf", f"{install_folder}/Setup.inf")
        shutil.copyfile(".venv/Inf_Sources/Setup.exe", f"{install_folder}/Setup.exe")
        shutil.copyfile(".venv/Inf_Sources/logo.bmp", f"{install_folder}/logo.bmp")
        shutil.copyfile(".venv/Inf_Sources/SyncFiles.ps1", f"{install_folder}/SyncFiles.ps1")

        # .msi in übergeordneten Ordner
        shutil.copyfile(temp_path, f"{source_folder}/{msifilename}")
    except Exception as e:
        return e

    # Alle Instanzen der search_words werden ersetzt
    final_inf = f"{install_folder}/Setup.inf"

    replace(final_inf, "[CURRENTDATE]", date)
    replace(final_inf, "[HERSTELLER]", hersteller)
    replace(final_inf, "[SOFTWARE]", software)
    replace(final_inf, "[VERSION]", version)
    replace(final_inf, "[REGKEY]", regkey)

    replace(final_inf, "[INSTALLER.msi]", msifilename)
    replace(final_inf, "[PROCESS]", software)

    # Paketierung zippen
    shutil.make_archive(parent_folder, "zip", "C:/temp/1_msi")

    # Zum Sparen von Speicherplatz auf dem Server - Uninitialisierung
    delete_file(temp_path)

    # Rückgabe von Oberpfad
    return f"{parent_folder}.zip"

def replace(inf_path, search_word, replacement_word):
    try:

        with open(inf_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Bearbeitung in "Zwischenspeicher"
        updated_content = content.replace(search_word, replacement_word)

        with open(inf_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        return True

    except Exception as e:
        logger.info("Bei replace()")
        logger.info(e)
        return False

# Funktionen zur Auslese der benötigten Daten aus der .msi
def get_date():
    date = datetime.date.today()
    day = date.strftime("%d")
    month = date.strftime("%m")
    year = date.strftime("%Y")
    return f"{day}.{month}.{year}"

def get_hersteller(temp_path):
    abfrage = search_entry("SELECT Value FROM Property WHERE Property = 'Manufacturer'", temp_path)

    result = (run_powershell(abfrage)).stdout.decode().strip()
    return result

def get_software(temp_path):
    abfrage = search_entry("SELECT Value FROM Property WHERE Property = 'ProductName'", temp_path)

    result = (run_powershell(abfrage)).stdout.decode().strip()
    return result

def get_version(temp_path):
    abfrage = search_entry("SELECT Value FROM Property WHERE Property = 'ProductVersion'", temp_path)

    result = (run_powershell(abfrage)).stdout.decode().strip()
    return result

def get_regkey(temp_path):
    abfrage = search_entry("SELECT Value FROM Property WHERE Property = 'ProductCode'", temp_path)

    result = (run_powershell(abfrage)).stdout.decode().strip()
    return result

# Aufruf von PowerShell - Rückgabe von Output
# Geringer Kompatibilität pywin32 mit Funktionen und mangelhafter Doku von Microsoft verschuldet
def run_powershell(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed

# PowerShell-Script mit Platzhaltern für alle Anfragen
def search_entry(query, temp_path):
    find_regkey_ps = f"""
        $windowsInstaller = New-Object -ComObject WindowsInstaller.Installer

        function Get-Property ($Object, $PropertyName, [object[]]$ArgumentList) {{
            return $Object.GetType().InvokeMember($PropertyName, 'Public, Instance, GetProperty', $null, $Object, $ArgumentList)
        }}

        $installer = $windowsInstaller.OpenDatabase("{temp_path}", 0)

        $view = $installer.OpenView("{query}")
        $view.Execute()

        $record = $view.Fetch()

        if ($record) {{
            Write-Output (Get-Property $record StringData 1)
        }}

        $view.Close()
        $installer.Commit()
        $installer = $null

        [system.gc]::Collect()
        [System.gc]::waitforpendingfinalizers()
        """

    return find_regkey_ps

# Nötig wegen Umgang mit .OpenDatabase
# Speichert eine hochgeladene Datei temporär und gibt den Dateipfad zurück.
def save_temp_file(file_storage, suffix=".msi"):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    file_storage.save(temp_file.name)
    temp_file.close()  # Datei wird nur geschrieben, nicht offen gehalten
    #logger.info(temp_file.name)
    return temp_file.name

# Löscht die temporäre Datei, wenn sie existiert.
def delete_file(filepath):
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass