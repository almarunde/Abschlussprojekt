# Abschlussprojekt
## Aufsetzen des Virtual Environments

Dies ist eine Anleitung zum Aufsetzen des Virtual Environments.

Dies ist vor der weiteren Installation von Flask und Co. auszuführen.

### Step 1 - Create an Environment
im Projekt-directory:

```sh
> py -3 -m venv .venv
```

### Step 2 - Activate the environment
dieses soll immer vor der Arbeit darin aktiviert werden.

```sh
> .venv\Scripts\activate
```

### Step 3 - Install Flask

```sh
> pip install flask --proxy=http://proxy.charite.de:8080
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
