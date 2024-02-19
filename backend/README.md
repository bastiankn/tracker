## Wichtig vor dem ersten Auführen

Vor dem ersten Ausführen des Codes müssen die Abhängigkeiten installiert werden. Dazu im Terminal folgendes eingeben:

- pip install -r requirements.txt

Damit die Datenbank erstellt wird muss die Datei init_db.py einmalig ausgeführt werden.

- cd backend
- python .\init_db.py


gutes Video:
https://www.youtube.com/watch?v=l9u_vm9aAmM

### Empfolene Erweiterungen für VS Code
- [alexcvzz.vscode-sqlite](https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite)
- [qwtel.sqlite-viewer](https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer)
- [mtxr.sqltools-driver-sqlite](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-sqlite)
- [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)


## Starten/Beenden der Applikation

starten mit:
- python .\app.py

beenden mit:
- Strg + C

## Misc
SQLAlchemy Query.get() ist deprecated, kann evtl. hiermit ersetzt werden:
https://stackoverflow.com/questions/75365194/sqlalchemy-2-0-version-of-user-query-get1-in-flask-sqlalchemy

## Venv

- pip list (= list of packages, that are installed)
- python -m venv [name]
- make sure that python is properly installed to the environment with python 
--version and pip --version
The following in Terminal
- virutalenv .venv
- .venv\Scripts\activate (You might have to enable running scripts in powershell: Open WindowsPowershell as admin, Get-ExecutionPolicy, if restricted: Set-ExecutionPolicy RemoteSigned)