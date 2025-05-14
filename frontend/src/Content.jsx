import './Content.css'

function Content() {
    return (
        <>
            <div id={"content"}>
                <p className={"absatz"}></p>
                <p className={"bigFont"}>Paketierungen erschaffen - auf einen Knopfdruck.</p>
                <p className={"kleinerAbsatz"}></p>
                <button className={"allButtons"} id={"hochladen"}>Datei hochladen</button>
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
                <p className={"infotext"}>Diese Website wurde im Rahmen des IHK-Abschlussprojekts der Ausbildungsrichtung Fachinformatik für
                    Anwendungsentwicklung erstellt und stellt durch diesen Rahmen bedingt nur die Funktionalität für
                    .msi-Softwarepaketierungen bereit.</p>
                <p className={"absatz"}></p>
            </div>
        </>

    )

}

export default Content