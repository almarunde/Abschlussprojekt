import './Header.css'
import Logo_Charite from "../assets/Logo_Charite.png"
import Pakulfus from "../assets/PaketierungsWizard.png"

function Header() {
    return (
        // Überlegung hier Logo und Pakulfus zu minimieren (logo siehe cd, pakulfus ohne schrift)
        <>
            <div id="header">
                <div id="linkeSpalte" className="spalten">
                    <img src={Logo_Charite} alt="Charité-Logo" id="logo"/>
                </div>
                <div id="mittlereSpalte" className="spalten"></div>
                <div id="rechteSpalte" className="spalten">
                    <img src={Pakulfus} alt="Paketierungstool Icon" id="pakulfus"/>
                    <div id="titelUndUntertitel">
                        <p id="titelTool">Paketierungstool</p>
                        <p id="untertitelTool">Abteilung Service und Support - Team Clientintegration</p>
                    </div>
                </div>
            </div>
        </>
    )

}

export default Header