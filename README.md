# Abschlussprojekt
## Voraussetzungen

Folgende Software muss auf deinem System installiert sein:

- [Pycharm](https://www.jetbrains.com/pycharm/download/?section=windows)
- [Git Bash](https://git-scm.com/downloads/win)
- [Python](https://www.python.org/downloads/)

## Initialisierung für Git-Konnektivität
Muss immer über git bash durchgeführt werden, sobald das Notebook wieder im Charité-Netz ist.

```bash
git config --global http.proxy http://proxy.charite.de:8080
```

## Aufsetzen des Virtual Environments

Dies ist eine Anleitung zum Aufsetzen des Virtual Environments.

Dies ist vor der weiteren Installation von Flask und Co. auszuführen.

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

## Aufsetzen des Frontends
## Voraussetzungen

Folgende Software muss auf deinem System installiert sein:

- [Node.js](https://nodejs.org/) (empfohlene Version: 22.12.0)
- [Yarn](https://yarnpkg.com/)
- [Angular CLI](https://angular.io/cli)

## Installation

Führe folgende Befehle aus, um das Projekt lokal einzurichten:

```sh
# Abhängigkeiten installieren
yarn install
```

## Entwicklung

Starte die Entwicklungsumgebung mit:

```sh
yarn start
```

Das Projekt wird unter `http://localhost:4200/` verfügbar sein.
