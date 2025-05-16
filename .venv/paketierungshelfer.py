import win32com.client

def create_package(msifile):
    '''
    TODO:
    Ersetzen von... mit ...:
    - [CURRENTDATE] mit current date
    - [HERSTELLER] mit AUSLESE ??? (kommt 2 mal vor)
    - [SOFTWARE] mit AUSLESE ??? (kommt 2 mal vor)
    - [VERSION] mit AUSLESE ??? (kommt 2 mal vor)
    - [REGKEY] mit AUSLESE ???
    - [INSTALLER.msi] mit Name der Installationsdatei
    - [PROCESS] - soll heißen wie Software

    => VIA pywin32 library von python
    => Eventuell Methodennamen etc abändern

    DIESE HIER WERDEN NOCH DAZUKOMMEN
    - [PROCESS.exe] - KANN ICH DAS ÜBERHAUPT RAUSFINDEN??
            alt notice an Nutzer, dass das ergänzt werden muss
    - [AppDir] - KANN ICH DAS AUSLESEN ????????
    '''



    return get_regkey(msifile)

def edit_msi():

    return

def get_regkey(msifile):
    installer = win32com.client.Dispatch("WindowsInstaller.Installer")
    db = installer.OpenDatabase(msifile, 0)  # 0 = read-only

    view = db.OpenView("SELECT Value FROM Property WHERE Property='ProductName'")
    view.Execute(None)
    record = view.Fetch()

    return record.StringData(1) if record else None