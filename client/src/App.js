// import './App.css';
// import './pages/CSS/Hero.css';
// import Hero from './pages/Hero';

// import Trackrecord from './pages/Trackrecord';
// import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

// function App() {
//   return (
//     <div className="App">
//       <Router>
//         <Routes>
//           <Route path="/myUFCAndPortfolio" element={<Hero />} />
//           <Route path="/myUFCAndPortfolio/trackrecord" element={<Trackrecord />} />
//         </Routes>
//       </Router>
//     </div>
//   );
// }
// export default App;

import React, { useState, useEffect } from 'react';
import Hero from './pages/Hero';
import Trackrecord from './pages/Trackrecord';
import About from './pages/About';
import axios from 'axios';
import './App.css';
import './pages/CSS/Navbar.css';
import './pages/CSS/Hero.css';

function App() {
    const [view, setView] = useState('about');
    const [activeButton, setActiveButton] = useState('about');
    const [fightData, setFightData] = useState([])
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get('https://ufc-picks-api-5897a84a5ddf.herokuapp.com/ufc_main_card')
            .then(response => {
                console.log(response.data)
                setFightData(response.data)
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching the main card data', error);
                setLoading(false);
            });
      }, []);
    const handleClick = (button) => {
      setActiveButton(button)
      setView(button)
    }

    return (
        <div className='App'>
            <nav className='nav-container'>
                <ul>
                    <li>
                        <button onClick={() => handleClick('about')} className={`boton-elegante ${activeButton === 'about' ? 'active' : ''}`}>About</button>
                    </li>
                    <li>
                        <button onClick={() => handleClick('hero')} className={`boton-elegante ${activeButton === 'hero' ? 'active' : ''}`}>Predictions</button>
                    </li>
                    <li>
                        <button onClick={() => handleClick('trackrecord')} className={`boton-elegante ${activeButton === 'trackrecord' ? 'active' : ''}`}>Track Record</button>
                    </li>
                </ul>
            </nav>
            <div>
                {view === 'hero' && !loading && <Hero fightData={fightData} />}
                {view === 'hero' && loading && <h2>Loading...</h2>}
                {view === 'trackrecord' && <Trackrecord />}
                {view === 'about' && <About />}
            </div>
        </div>
    );
}

export default App;