import os
import shutil

from flask import Flask, request, send_file, make_response
from flask_cors import CORS
from paketierungshelfer import create_package

import logging

logging.basicConfig(
    level=logging.INFO,  # Oder DEBUG für mehr Details
    format='%(asctime)s [%(levelname)s] %(message)s'
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'])  # Cross-Origin Resource Sharing

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/fileToBackend', methods=['POST'])
def upload_file():
    logger.info('Started')
    msifile = request.files.get('file')
    msifilename = request.form.get('filename', 'unbekannt')

    if ".msi" in msifilename:
        # Soll Pfad zur zip enthalten
        return create_package(msifile, msifilename)
    elif ".exe" in msifilename:
        return {'message': '.exe'}, 200

    return {'message': f'Datei {msifilename} empfangen'}, 200

@app.route('/download')
def download():
    file_path = request.args.get('path')
    filename = os.path.basename(file_path)

    response = make_response(send_file(file_path, as_attachment=True))
    response.headers["X-File-Name"] = filename  # Neuer Header
    response.headers["Access-Control-Expose-Headers"] = "X-File-Name"  # Damit JS ihn lesen darf
    return response

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
