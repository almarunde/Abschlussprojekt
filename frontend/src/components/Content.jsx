import './Content.css'
import React, {useState} from "react";
import axios from "axios";

function Content() {

    const enableHochladenButton = () => {
        document.getElementById("hochladenButton").disabled = false;
    }

    const disableHochladenButton = () => {
        document.getElementById("hochladenButton").disabled = true;
    }

    const [selectedFile, setSelectedFile] = useState(null)

    // Setzt selectedFile bei neuer Dateiauswahl
    const onFileChange = (event) => {
        setSelectedFile(event.target.files[0])
    }

    // Erstellt FormData Objekt mit Datei im Anhang
    // Durch Button-Disabling nur bei richtigen Dateien
    const onFileUpload = () => {

        // Why needed
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('filename', selectedFile.name);

        axios.post('http://localhost:5000/fileToBackend', formData)
    }

    // Identifiziert Dateityp anhand Namen
    const identifyFile = () => {
        if (selectedFile) {
            let name = selectedFile.name.toString()

            // Da später noch überprüft werden muss, welcher Dateityp das ist
            // - Überlegung hier nur Handling von nicht-msi und exe
            if (name.includes(".msi")) {
                enableHochladenButton()
                return (
                    <div className={"ueberschriften"}>Datei ist eine .msi</div>
                )
            } else if (name.includes(".exe")) {
                enableHochladenButton()
                return (
                    <div className={"ueberschriften"}>Datei ist eine .exe</div>
                )
            } else {
                disableHochladenButton()
                return (
                    <div className={"ueberschriften"}>Ungültiger Dateityp!</div>
                )
            }
        }
    }

    return (
        <>
            <div id={"content"}>
                <p className={"absatz"}></p>
                <p className={"bigFont"}>Paketierungen erschaffen - auf einen Knopfdruck.</p>
                <p className={"kleinerAbsatz"}></p>

                <input type="file" onChange={onFileChange}/>
                <p className={"kleinerAbsatz"}></p>
                <div>{identifyFile()}</div>
                <p className={"kleinerAbsatz"}></p>
                <button className={"allButtons"} id={"hochladenButton"} onClick={onFileUpload}>Paketierung erstellen
                </button>

                <p className={"absatz"}></p>
                <p className={"ueberschriften"}>Bedienungsanleitung:</p>
                <p className={"kleinerAbsatz"}></p>
                <div id={"threeRows"}>
                    <div className={"anleitungsText"}>1) Laden Sie eine Installationsdatei mit dem Dateitypen .msi oder
                        .exe hoch.
                    </div>
                    <div className={"anleitungsText"}>2) Das Paketierungstool bereitet für Sie in sekundenschnelle ein
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