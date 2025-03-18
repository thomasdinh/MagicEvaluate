import '../css/DeckCard.css'

function DeckCard({deck}){

    function onInfoClick(){
        alert("clicked")
    }

    return (
    <div className = "DeckCard">
        <div className="deck_poster">
            <img src="https://cards.scryfall.io/art_crop/front/6/7/673c21f8-02b6-4ac4-b2fc-df065b4ac662.jpg?1726285172" alt=" deck.name"></img>
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