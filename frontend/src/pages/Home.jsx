import DeckCard from "../components/DeckCard"
import { useEffect, useState, useMemo } from "react";
import "../css/Home.css"
import { getDecks } from "../services/api";
import SortPicker from "../components/SortPicker";

function Home(){

    const [searchQuery, setSearchQuery] = useState ("");
    const [decks, setDecks] = useState([]);
    const [sortOrder, setSortOrder] = useState("name_asc"); 
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect( () =>{
        const loadYourDecks = async () =>{
            try{
                const decks = await getDecks()
                setDecks(decks)
            }catch (err){
                console.log(err)
                setError("Failed to load...")
            }
            finally{
                setLoading(false)
            }
    
        }
        loadYourDecks()
    }, [])

    useEffect(()=>{
        console.log('Changed sort order.')
    },[sortOrder]);

    const handleSearch = () =>{};

    // Sorting function
    const sortedDecks = useMemo(() => {
        return [...decks].sort((a, b) => {
            switch (sortOrder) {
                case "name_asc":
                    return a.name.localeCompare(b.name);
                case "name_desc":
                    return b.name.localeCompare(a.name);
                case "asc_winrate":
                    return parseFloat(a.winrate) - parseFloat(b.winrate);
                case "desc_winrate":
                    return parseFloat(b.winrate) - parseFloat(a.winrate);
                default:
                    return 0;
            }
        });
    }, [decks, sortOrder]);

    return (
        <div className="home">
            <SortPicker onChange={(e) => setSortOrder(e.target.value)} />

            <form onSubmit={(e) => handleSearch()} className="search-form">
                <input
                    type="text"
                    placeholder="Search for Decks..."
                    className="input_search_home"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button type="submit" className="searchButton" onClick={null}>Search</button>
            </form>

            <div className="deck-grid">
                {sortedDecks.map((deck) =>
                    deck.name.toLowerCase().includes(searchQuery.toLowerCase()) ? (
                        <DeckCard deck={deck} key={deck.id} />
                    ) : null
                )}
            </div>
        </div>
    );
}

export default Home