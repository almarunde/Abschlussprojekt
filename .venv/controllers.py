from flask import Flask, request
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
        return create_package(msifile)
    elif ".exe" in msifilename:
        return {'message': '.exe'}, 200

    return {'message': f'Datei {msifilename} empfangen'}, 200


# Versichert Ausführung bei direktem Start
if __name__ == '__main__':
    app.run(debug=True)
