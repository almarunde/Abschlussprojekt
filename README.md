# Abschlussprojekt
## Voraussetzungen

Folgende Software muss auf deinem System installiert sein:

- Backend:
  - [Pycharm](https://www.jetbrains.com/pycharm/download/?section=windows)
  - [Git Bash](https://git-scm.com/downloads/win)
  - [Python](https://www.python.org/downloads/)
  - Flask and Flask_CORS (siehe Backend Schritt 4 & 5)
  - pywin32 (ÜBERLEGEN OB DIESE NUR UNTEN ERWÄHNT WERDEN SOLLEN)
- Frontend:
  - [Node.js](https://nodejs.org/)
  - Axios ( via ```npm i axios --save``` )

## Proxy konfigurieren
Muss **immer über git bash** durchgeführt werden, sobald das Notebook wieder im Charité-Netz ist.

### Mit Git:
```git bash
# Execute in git bash!!!
git config --global http.proxy http://proxy.charite.de:8080
```

### Mit npm:
```git bash
# Execute in git bash!!!
npm config set proxy http://proxy.charite.de:8080
npm config set https-proxy http://proxy.charite.de:8080
```

## Aufsetzen des Backends (Flask) - http://localhost:5000
## Aufsetzen des Virtual Environments

Dies ist eine Anleitung zum Aufsetzen des Virtual Environments und ist vor der weiteren Installation von Flask und Co. auszuführen.

### Step 1 - Create an Environment
im Projekt-directory:

```sh
py -3 -m venv .venv
```

### Step 2 - Activate the environment
dieses soll immer vor der Arbeit darin aktiviert werden.

```sh
.venv\Scripts\activate
```

### Step 3 - Install Flask

```sh
pip install flask --proxy=http://proxy.charite.de:8080
```

### Step 4 - Install Flask CORS
```sh
pip install flask-cors --proxy=http://proxy.charite.de:8080
```
Danach noch in IDE dafür sorgen, dass Paket definitiv installiert ist.

### Step 5 - Install pywin32
```sh
pip install pywin32 --proxy=http://proxy.charite.de:8080
```
Danach noch in IDE dafür sorgen, dass Paket definitiv installiert ist.

## Starten des Backends
Nach Aktivierung der .venv:
```sh
flask --app controllers run
```
Danach noch in IDE dafür sorgen, dass Paket definitiv installiert ist.

Das Projekt wird unter `http://localhost:5000/` verfügbar sein.

## Aufsetzen des Frontends (React) - http://localhost:5173
## Installation

```git bash
# Execute in git bash!!!
npm create vite@latest frontend -- --template react
```

## Entwicklung

Starte die Entwicklungsumgebung mit:

```git bash
# Execute in git bash!!!
cd frontend
npm install
npm run dev
```
Die Ausführung von npm Install ist nur beim ersten Mal wirklich nötig - kann aber nicht schaden

Das Projekt wird unter `http://localhost:5173/` verfügbar sein.
