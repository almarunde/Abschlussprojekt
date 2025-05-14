import './Header.css'
import Logo_Charite from "./assets/Logo_Charite.png"
import Pakulfus from "./assets/PaketierungsWizard.png"

function Header() {
    return (
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