import './Content.css'
import React, {useEffect, useState} from "react";
import axios from "axios";
import {ClipLoader} from "react-spinners";

function Content() {

    const [selectedFile, setSelectedFile] = useState(null)
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

    // Erstellt FormData Objekt mit Datei im Anhang
    // Durch Button-Disabling nur bei richtigen Dateien
    const onFileUpload = () => {
        console.log("Upload-Funktion wurde aufgerufen");
        if (selectedFile) {
            document.getElementById("isPackaging").style.display = "inline";
            setLoading(true);
            document.getElementById("hochladenButton").style.display = "none";

            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('filename', selectedFile.name);

            axios.post("http://localhost:5000/fileToBackend", formData)
                .then(res => {
                    setFilePath(res.data);
                    setLoading(false);
                    document.getElementById("isPackaging").style.display = "none";
                    console.log("Backend-Antwort:", res.data);

                    // Download erst nach Erfolg ermöglichen
                    document.getElementById("packageDone").style.display = "inline";
                    document.getElementById("downloadButton").style.display = "inline";
                })
                .catch(err => console.error("Fehler beim Backend-Call:", err));

        } else {
            // entweder hier show von error im fe oder immediately disabled haben
            console.log("Erstellungsversuch ohne Datei");
        }
    }

    const onFileDownload = async () => {
        try {
            const response = await axios.get(`http://localhost:5000/download?path=${filePath}`, {
                responseType: 'blob',
            });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'Paketierung.zip');
            document.body.appendChild(link);
            link.click();
            link.remove();

            // Cleanup call
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

    // onFileUpload erst ermöglichen, wenn Dateityp ok, ohne render-Fehler zu triggern
    useEffect(() => {
        if (!selectedFile) {
            setIsUploadDisabled(true);
            return;
        }

        const name = selectedFile.name;

        if (name.endsWith(".msi")) {
            setIsUploadDisabled(false);
        } else if (name.endsWith(".exe")) {
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
                <div><ClipLoader loading={loading} color="#123abc" size={70}/></div>
                <p id={"isPackaging"}>Ihr Paket wird erstellt...</p>
                <p id={"packageDone"}>Ihr Paket wurde erstellt und steht Ihnen nun zum Download bereit.</p>
                <p className={"kleinerAbsatz"}></p>
                <button className={"allButtons"} id={"hochladenButton"} onClick={onFileUpload}
                        disabled={isUploadDisabled}>Paketierung erstellen
                </button>
                <button className={"allButtons"} id={"downloadButton"} onClick={onFileDownload}>Paketierung
                    runterladen
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