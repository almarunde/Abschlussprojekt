# Abschlussprojekt
## Voraussetzungen

Folgende Software muss manuell auf dem System installiert sein:

- Backend:
  - [Pycharm](https://www.jetbrains.com/pycharm/download/?section=windows)
  - [Git Bash](https://git-scm.com/downloads/win)
  - [Python](https://www.python.org/downloads/)
- Frontend:
  - [Node.js](https://nodejs.org/)

## Proxy konfigurieren
Muss **immer über git bash** durchgeführt werden, sobald das Notebook wieder im Charité-Netz ist.
Außerdem muss der proxy auch in der IDE eingestellt sein.

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

### Step 5 - Install PowerShell Plugin in IDE
Unter File -> Settings -> Plugins -> PowerShell installieren

### Step 6 - Install React-Spinners
Die IDE erkennt nicht unbedingt direkt, dass diese Installation auch mit dem proxy läuft - so umgeht man darauf bezogene Probleme.

```sh
npm install react-spinners --save --proxy http://proxy.charite.de:8080
```

## Starten des Backends
Nach Aktivierung der .venv:
```sh
flask --app controllers run --debug
```

Das Projekt wird unter `http://localhost:5000/` verfügbar sein.

## Aufsetzen des Frontends (Vite with React) - http://localhost:5173
## Installation 
### Vite und React

```git bash
# Execute in git bash!!!
npm create vite@latest frontend -- --template react
```

Hier auswählen, dass bestehende Dateien ignoriert werden sollen - danach rollback via Git-Fenster.

### Axios
```git bash
# Execute in git bash!!!
npm i axios --save
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

## Für hostenden Server:

Füge in vite.config.js den folgenden Abschnitt hinzu, um es via dieser IP-Adresse zu hosten:
```
server: {
    host: true,
    allowedHosts: ['paketierungstool']
  }
```
Der Abschnitt um allowedHosts ermöglicht, die Seite via http://paketierungstool:5173/ einzusehen - und nicht nur über die hostende IP-Adresse.
Dafür muss aber beim Client die IP-Adresse unter C:\Windows\System32\drivers\etc\hosts mit der entsprechenden Namensauflösung hinterlegt sein.

## Wichtiges Extra: Zur Entlastung des Speicherplatz des Servers: Aufgabenplanung Paket-Cache leeren

1. Dateien unter "extras" hier im Projekt nach C:\ProgramData\#Paketierungshelfer verschieben
2. Aufgabenplanung öffnen
3. Auf "Aufgabe importieren..." --> EmptyPackageCache.xml reinladen
4. 'OK' drücken