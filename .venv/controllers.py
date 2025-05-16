from flask import Flask, request
from flask_cors import CORS
import paketierungshelfer

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'])  # Cross-Origin Resource Sharing

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/fileToBackend', methods=['POST'])
def upload_file():
    msifile = request.files.get('file')
    msifilename = request.form.get('filename', 'unbekannt')

    if ".msi" in msifilename:
        return {'message': f'Datei {msifilename} empfangen - regkey ist: '}, 200
    elif ".exe" in msifilename:
        return ".exe"

    return {'message': f'Datei {msifilename} empfangen'}, 200


# Versichert Ausführung bei direktem Start
if __name__ == '__main__':
    app.run(debug=True)
