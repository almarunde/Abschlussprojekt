# Abschlussprojekt
## Voraussetzungen

Folgende Software muss auf deinem System installiert sein:

- Backend:
  - [Pycharm](https://www.jetbrains.com/pycharm/download/?section=windows)
  - [Git Bash](https://git-scm.com/downloads/win)
  - [Python](https://www.python.org/downloads/)
- Frontend:
  - [Node.js](https://nodejs.org/)

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

## Aufsetzen des Backends (Flask) - http://localhost:???
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

Das Projekt wird unter `http://localhost:5173/` verfügbar sein.
