import shutil
import subprocess
import datetime
import tempfile
import os
import logging
from pathlib import Path

# Für Arbeit im Backend und Troubleshooting
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Hier ganze Logik zu Auslese und .inf-Anpassung integriert
def create_package(msifile, msifilename, email, appDir, processName):
    temp_path = save_temp_file(msifile)

    # Alle wichtigen Daten (u.A. aus .msi) auslesen
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

    # Vorschrieb-inf kopieren für zu-editierende-inf
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

    # Hier die aus dem Frontend übernommenen Instanzen übergeben:
    replace(final_inf, "[AUTHOR]", email)
    replace(final_inf, "[APPDIR]", appDir)
    replace(final_inf, "[PROCESS.exe]", processName)

    # Paketierung zippen
    # Aufbau von shutil.make_archive() durch KI erklären lassen
    zip_path = shutil.make_archive(
        base_name=parent_folder,
        format="zip",
        root_dir=parent_folder,
        base_dir="."
    )

    # Zum Sparen von Speicherplatz auf dem Server - Löschung von temp-msi
    delete_file(temp_path)

    # Rückgabe von Oberpfad
    return f"{zip_path}"

# Hier Logik zum Ersetzen von Teilen der .inf
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

### Funktionen zur Auslese der benötigten Daten aus der .msi: ###
# Datum auslesen
def get_date():
    date = datetime.date.today()
    day = date.strftime("%d")
    month = date.strftime("%m")
    year = date.strftime("%Y")
    return f"{day}.{month}.{year}"

# Herstellername auslesen
def get_hersteller(temp_path):
    abfrage = search_entry("SELECT Value FROM Property WHERE Property = 'Manufacturer'", temp_path)

    result = (run_powershell(abfrage)).stdout.decode().strip()
    return result

# Softwarename auslesen
def get_software(temp_path):
    abfrage = search_entry("SELECT Value FROM Property WHERE Property = 'ProductName'", temp_path)

    result = (run_powershell(abfrage)).stdout.decode().strip()
    return result

# Versionsnummer auslesen
def get_version(temp_path):
    abfrage = search_entry("SELECT Value FROM Property WHERE Property = 'ProductVersion'", temp_path)

    result = (run_powershell(abfrage)).stdout.decode().strip()
    return result

# RegKey auslesen
def get_regkey(temp_path):
    abfrage = search_entry("SELECT Value FROM Property WHERE Property = 'ProductCode'", temp_path)

    result = (run_powershell(abfrage)).stdout.decode().strip()
    return result

# Aufruf von PowerShell-Befehlen
def run_powershell(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed

# PowerShell-Script mit Platzhaltern für alle Auslese-Anfragen
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
# Speichert eine hochgeladene Datei temporär und gibt den Dateipfad zurück
# tempfile-Modul durch KI herausgefunden
def save_temp_file(file_storage, suffix=".msi"):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    file_storage.save(temp_file.name)
    temp_file.close()  # Datei wird nur geschrieben, nicht offen gehalten
    return temp_file.name

# Löscht die temporäre Datei, wenn sie existiert
def delete_file(filepath):
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass