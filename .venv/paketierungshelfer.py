
import gc
import subprocess
import winreg

import pythoncom
import win32com.client
import tempfile
import os
import logging

logging.basicConfig(
    level=logging.INFO,  # Oder DEBUG für mehr Details
    format='%(asctime)s [%(levelname)s] %(message)s'
)

logger = logging.getLogger(__name__)

from flask import jsonify

'''
def create_package(msifile):
    
    TODO:
    Ersetzen von... mit ...:
    - [CURRENTDATE] mit current date
    - [HERSTELLER] mit AUSLESE ??? (kommt 2 mal vor)
    - [SOFTWARE] mit AUSLESE ??? (kommt 2 mal vor)
    - [VERSION] mit AUSLESE ??? (kommt 2 mal vor)
    - [REGKEY] mit AUSLESE ???
    - [INSTALLER.msi] mit Name der Installationsdatei
    - [PROCESS] - soll heißen wie Software

    => VIA pywin32 library von python
    => Eventuell Methodennamen etc abändern

    DIESE HIER WERDEN NOCH DAZUKOMMEN
    - [PROCESS.exe] - KANN ICH DAS ÜBERHAUPT RAUSFINDEN??
            alt notice an Nutzer, dass das ergänzt werden muss
    - [AppDir] - KANN ICH DAS AUSLESEN ????????
    
'''


def create_package(msifile):
    logger.info('Methode wird aufgerufen')

    temp_path = save_temp_file(msifile)

    db = None
    installer = None

    # "Datenbank" der .msi öffnen, um Daten auszulesen
    try:
        logger.info('createpackage try wird aufgerufen')
        pythoncom.CoInitialize()

        #installer = win32com.client.gencache.EnsureDispatch("WindowsInstaller.Installer")
        installer = win32com.client.Dispatch("WindowsInstaller.Installer")

        logger.info("installer start")
        logger.info(installer)
        logger.info("type:")
        logger.info(type(installer))
        logger.info("dir:")
        logger.info(dir(installer))

        db = installer.OpenDatabase(temp_path, 0)  # 0 = read-only
        logger.info("db1 start")
        logger.info(db)
        logger.info(type(db))
        logger.info(dir(db))
        regkey = get_regkey(db)
        logger.info('createpackage try wird komplett durchgegangen')
        return jsonify({'message': str(regkey)}), 200
    except Exception as e:
        logger.info('exception occured')
        logger.info(e)
        return jsonify({'error': str(e)}), 500
    finally:
        db = None
        installer = None
        gc.collect()
        pythoncom.CoUninitialize()
        delete_file(temp_path)


def get_regkey(db):


    view = db.OpenView("SELECT * FROM `Property`")
    view.Execute()
    record = view.Fetch()

    logger.info("db start")
    logger.info(db)
    logger.info(type(db))
    logger.info(dir(db))

    logger.info("view start")
    logger.info(view)
    logger.info(type(view))
    logger.info(dir(view))

    logger.info("record start")
    logger.info(record)
    logger.info(record.StringData)
    logger.info(type(record))
    logger.info(dir(record))
    propval = record.StringData
    logger.info(propval)
    return "Durchgelaufen"

def run_powershell(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed

# Nötig wegen Umgang mit .OpenDatabase
# Speichert eine hochgeladene Datei temporär und gibt den Dateipfad zurück.
def save_temp_file(file_storage, suffix=".msi"):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    file_storage.save(temp_file.name)
    temp_file.close()  # Datei wird nur geschrieben, nicht offen gehalten
    logger.info(temp_file.name)
    return temp_file.name

# Löscht die temporäre Datei, wenn sie existiert.
def delete_file(filepath):
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass
