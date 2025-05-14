import './Header.css'
import Logo_Charite from "../assets/Logo_Charite.png"
import Pakulfus from "../assets/PaketierungsWizard.png"

function Header() {
    return (
        // Überlegung hier Logo und Pakulfus zu minimieren (logo siehe cd, pakulfus ohne schrift)
        <>
            <div id={"header"}>
                <div id={"linkeSpalte"} className={"spalten"}><img src={Logo_Charite} id={"logo"}></img></div>
                <div id={"mittlereSpalte"} className={"spalten"}></div>
                <div id={"rechteSpalte"} className={"spalten"}><img src={Pakulfus} id={"pakulfus"}/>
                    <p id={"titelTool"}>Paketierungstool</p>
                    <p id={"untertitelTool"}>Abteilung Service und Support - Team Clientintegration</p>
                </div>
            </div>
        </>
    )

}

export default Header