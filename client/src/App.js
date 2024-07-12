import './App.css';
import './pages/CSS/Hero.css';
import Hero from './pages/Hero';
import { BrowserRouter as Router} from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Router>
        <Hero/>
      </Router>
    </div>
  );
}

export default App;
