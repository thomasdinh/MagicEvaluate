import DeckCard from "../components/DeckCard"
import { useState } from "react";

function Home(){
    const [searchQuery, setSearchQuery] = useState ("");

    const decks = [
        {deck_id: 1, name: "Aesi", winrate: "50.00"},
        {deck_id: 2, name: "Pantlaza", winrate: "15.00"},
        {deck_id: 3, name: "Kaalia", winrate: "20.00"},
        {deck_id: 4, name: "Temmet", winrate: "0.00"},
        {deck_id: 5, name: "aehomas", winrate: "100.00"},
    ] 

    const handleSearch = () =>{};

    return (
    <div className="home">
        <form onSubmit={handleSearch} className="search-form">
            <input type="text" 
            placeholder="Search for Decks..."
            className="input_search_home"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button type="submit" className="searchButton"> Search</button>
        </form>

        <div className="deck-grid">
        {decks.map((deck) => 
            {
                if (deck.name.toLowerCase().startsWith(searchQuery)) {
                    return <DeckCard deck={deck} key={deck.deck_id} />;
                }   
                else{
                    return null; // Return null if the condition is not met
                }
            }
        )}
        </div>
    </div>
    )
}

export default Home