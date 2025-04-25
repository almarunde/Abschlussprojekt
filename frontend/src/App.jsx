import { useState } from 'react'
import './App.css'
import Header from "./Header.jsx";

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
          <Header/>
      </div>
      <h1>Welcome page</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>

      </div>
    </>
  )
}

export default App
