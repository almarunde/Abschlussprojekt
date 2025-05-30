import os
import shutil

from flask import Flask, request, send_file, make_response
from flask_cors import CORS
from paketierungshelfer import create_package

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'])  # Cross-Orgin Resource Sharing - für Front- und Backend-Verbindung

# Ausschließlich zum Testen von Erreichbarkeit
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Hierunter alles zur Paketierungserstellung selbst
@app.route('/fileToBackend', methods=['POST'])
def upload_file():
    logger.info('Started')
    msifile = request.files.get('file')
    msifilename = request.form.get('filename', 'unbekannt')
    email = request.form.get('email', 'unbekannt')
    appDir = request.form.get('appDir', 'unbekannt')
    processName = request.form.get('processName', 'unbekannt')

    if ".msi" in msifilename:
        # Soll Pfad zur zip enthalten
        return create_package(msifile, msifilename, email, appDir, processName)
    elif ".exe" in msifilename:
        return {'message': '.exe'}, 200

    return {'message': f'Datei {msifilename} empfangen'}, 200

# Hierunter alles Nötige zum Download
@app.route('/download')
def download():
    file_path = request.args.get('path')
    filename = os.path.basename(file_path)

    response = make_response(send_file(file_path, as_attachment=True))
    response.headers["X-File-Name"] = filename  # Neuer Header
    response.headers["Access-Control-Expose-Headers"] = "X-File-Name"  # Damit JS ihn lesen darf
    return response

# Hierunter alles zum regulär gewollten cleanup
@app.route('/cleanup', methods=['POST'])
def cleanup():
    data = request.json
    file_path = data.get("path")
    base_folder = file_path.replace(".zip", "")

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(base_folder):
            shutil.rmtree(base_folder)
        return "Cleanup erfolgreich", 200
    except Exception as e:
        return str(e), 500

# Versichert Ausführung bei direktem Start
if __name__ == '__main__':
    app.run(debug=True)
