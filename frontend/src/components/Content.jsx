import './Content.css'
import React, {useEffect, useState} from "react";
import axios from "axios";
import {ClipLoader} from "react-spinners";

function Content() {

    const [selectedFile, setSelectedFile] = useState(null)
    const [email, setEmail] = useState(null)
    const [appDir, setAppDir] = useState(null)
    const [processName, setProcessName] = useState(null)

    const [loading, setLoading] = useState(false);
    const [filePath, setFilePath] = useState(null);
    const [isUploadDisabled, setIsUploadDisabled] = useState(true);

    // Setzt selectedFile bei neuer Dateiauswahl
    const onFileChange = (event) => {
        const file = event.target.files[0];
        if (!file) {
            console.log("Keine Datei erkannt")
            return;
        }
        setSelectedFile(file);
    }

    // Zum Anzeigen des Formulars
    const toUserEntry = () => {
        document.getElementById("paketierungStarten").style.display = "none";
        document.getElementById("formular").style.display = "flex";
        document.getElementById("hochladenButton").style.display = "flex";
    }

    // Weiterleitung zu Paketerstellungslogik
    // Durch Button-Disabling nur bei richtigen Dateien
    const onFileUpload = (e) => {
        // Verhindert URL-Anpassung
        e.preventDefault();

        if (selectedFile) {
            document.getElementById("formular").style.display = "none";
            document.getElementById("isPackaging").style.display = "inline";
            setLoading(true);
            document.getElementById("hochladenButton").style.display = "none";

            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('filename', selectedFile.name);
            formData.append('email', email)
            formData.append('appDir', appDir)
            formData.append('processName', processName)

            axios.post("http://localhost:5000/fileToBackend", formData)
                .then(res => {
                    setFilePath(res.data);
                    setLoading(false);
                    document.getElementById("isPackaging").style.display = "none";

                    // Download erst nach Erfolg ermöglichen
                    document.getElementById("packageDone").style.display = "inline";
                    document.getElementById("informUser").style.display = "inline";
                    document.getElementById("downloadButton").style.display = "inline";
                })
                .catch(err => console.error("Fehler beim Backend-Call:", err));

        } else {
            console.log("Erstellungsversuch ohne Datei");
        }
    }

    // Download starten
    const onFileDownload = async () => {
        try {
            const response = await axios.get(`http://localhost:5000/download?path=${filePath}`, {
                responseType: 'blob',
            });

            // Neuen Header lesen
            let filename = response.headers['x-file-name'] || 'fallback.zip';

            const blob = new Blob([response.data], {type: 'application/zip'})

            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            link.remove();

            // Cleanup
            await axios.post("http://localhost:5000/cleanup", {
                path: filePath
            });

            console.log("Server-Dateien gelöscht");
            document.getElementById("downloadButton").style.display = "none";
            document.getElementById("neuePaketierungButton").style.display = "inline";

        } catch (err) {
            console.error("Fehler beim Herunterladen oder Bereinigen:", err);
        }
    }

    // onFileUpload beim ersten Render schon nicht einfach so ermöglichen
    useEffect(() => {
        if (!selectedFile) {
            setIsUploadDisabled(true);
            return;
        }

        const name = selectedFile.name;

        if (name.endsWith(".msi")) {
            setIsUploadDisabled(false);
        } else if (name.endsWith(".exe")) {
            // Bis Funktion gewährleistet wird
            setIsUploadDisabled(true);
        } else {
            setIsUploadDisabled(true);
        }
    }, [selectedFile]);

    return (
        <>
            <div id={"content"}>
                <p className={"absatz"}></p>
                <p className={"bigFont"}>Paketierungen erschaffen - auf einen Knopfdruck.</p>
                <p className={"kleinerAbsatz"}></p>

                <input type="file" accept={".msi, .exe"} onChange={onFileChange}/>
                <p className={"kleinerAbsatz"}></p>

                <form id={"formular"} onSubmit={onFileUpload}>
                    <div className={"form-row"}>
                        <p className={"progressText"} id={"infoNeeded"}>Vor Paketierungsabschluss, benötigen wir von
                            Ihnen noch ein paar Informationen:</p>
                    </div>
                    <div className={"form-row"}>
                        <label>Email-Adresse: *</label>
                        <input type="email"
                               name="email"
                               required={true}
                               onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                    <div className={"form-row"}>
                        <label>ApplicationDir der Anwendung: *</label>
                        <input required={true} onChange={(e) => setAppDir(e.target.value)}/>
                    </div>
                    <div className={"form-row"}>
                        <label>Prozessname der Anwendung: *</label>
                        <input required={true} onChange={(e) => setProcessName(e.target.value)}/>
                    </div>
                    <button type={"submit"} className={"allButtons"} id={"hochladenButton"}
                            disabled={isUploadDisabled}>Paketierung erstellen
                    </button>
                </form>

                <div><ClipLoader loading={loading} color="#123abc" size={70}/></div>
                <p className={"progressText"} id={"isPackaging"}>Ihr Paket wird erstellt...</p>
                <p className={"progressText"} id={"packageDone"}>Ihr Paket wurde erstellt und steht Ihnen nun zum
                    Download bereit.</p>
                <p></p>
                <p className={"progressText"} id={"informUser"}>Bitte überprüfen Sie die Richtigkeit aller Daten und
                    passen das Paket ggfs. an.</p>
                <p className={"kleinerAbsatz"}></p>
                <button className={"allButtons"} id={"paketierungStarten"} onClick={toUserEntry}
                        disabled={isUploadDisabled}>Paketierung starten
                </button>
                <button className={"allButtons"} id={"downloadButton"} onClick={onFileDownload}>Paketierung
                    herunterladen
                </button>
                <button className={"allButtons"} id={"neuePaketierungButton"} onClick={() => window.location.reload()}>
                    Neue Paketierung erstellen
                </button>

                <p className={"absatz"}></p>
                <p className={"ueberschriften"}>Bedienungsanleitung:</p>
                <p className={"kleinerAbsatz"}></p>
                <div id={"threeRows"}>
                    <div className={"anleitungsText"}>1) Laden Sie eine Installationsdatei mit dem Dateitypen .msi
                        oder
                        .exe hoch.
                    </div>
                    <div className={"anleitungsText"}>2) Das Paketierungstool bereitet für Sie in sekundenschnelle
                        ein
                        fertiges Paket zu.
                    </div>
                    <div className={"anleitungsText"}>3) Das fertige Paket wird Ihnen als .zip-Datei bereitgestellt,
                        welche Sie anschließend runterladen können.
                    </div>
                </div>
                <p className={"kleinerAbsatz"}></p>
            </div>
            <div id={"aktuelles"}>
                <p className={"ueberschriften"}>Aktuelles:</p>
                <p className={"kleinerAbsatz"}></p>
                <p className={"infotext"}>Diese Website wurde im Rahmen des IHK-Abschlussprojekts der
                    Ausbildungsrichtung Fachinformatik für
                    Anwendungsentwicklung erstellt und stellt durch diesen Rahmen bedingt nur die Funktionalität für
                    .msi-Softwarepaketierungen bereit.</p>
                <p className={"absatz"}></p>
            </div>
        </>

    )

}

export default Content