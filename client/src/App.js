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

import React, { useState } from 'react';
import Hero from './pages/Hero';
import Trackrecord from './pages/Trackrecord';
import About from './pages/About';
import './App.css';
import './pages/CSS/Navbar.css';
import './pages/CSS/Hero.css';

function App() {
    const [view, setView] = useState('about');
    const [activeButton, setActiveButton] = useState('about');

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
                {view === 'hero' && <Hero />}
                {view === 'trackrecord' && <Trackrecord />}
                {view === 'about' && <About />}
            </div>
        </div>
    );
}

export default App;