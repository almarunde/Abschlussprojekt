import {useState} from 'react'
import './App.css'
import Header from "./Header.jsx";
import Content from "./Content.jsx";
import Footer from "./Footer.jsx";

function App() {
    const [count, setCount] = useState(0)
    // das hier wegmachen, ist hier nur als reference

    return (
        <>

            <Header/>
            <Content/>
            <Footer />
            <h1>Welcome page</h1>
            <div className="card">
                <button onClick={() => setCount((count) => count + 1)}>
                    count is {count}
                </button>

            </div>
        </>
    );
}

export default App
