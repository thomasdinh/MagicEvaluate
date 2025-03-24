import '../css/DeckCard.css'

function DeckCard({deck}){

    function onInfoClick(){
        alert("clicked")
    }

    return (
    <div className = "DeckCard">
        <div className="deck_poster">
            <img src={deck.url} alt="src/assets/magic_commander_deck.png" onError={() => setImgSrc("src/assets/magic_commander_deck.png")}></img>
            <div className="deck-overlay">
                <button className="info_button" onClick={onInfoClick}> 
                    <sup>&#9432;</sup> 
                </button>
            </div>
        </div>
        <div className="deck_info">
            <h3>{deck.name}</h3>
            <p>{deck.winrate.toFixed(2)}%</p>
        </div>
    </div>
    )
}

export default DeckCard;