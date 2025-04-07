import { Link } from "react-router-dom"
import '../css/NavBar.css';


function Navbar(){
    return(
    <nav>
        <div className="navbar">
            <Link to="/">Deck Track App</Link>
        </div>
        <div className="navbar-links">
            <Link to="/" className="nav-link">Home</Link>
            <Link to="/yourdecks" className="nav-link">Your Decks</Link>

        </div>

    </nav>);
}

export default Navbar;