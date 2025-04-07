export const getDecks = async () => {
    const BASE_URL = 'https://magicevaluate.onrender.com/all_decks'; // Update with your FastAPI server URL http://localhost:8000 for local
    const SCRYFALL_URL = 'https://api.scryfall.com/cards/search?q='

    try {
        const response = await fetch(BASE_URL);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        return data;
    } catch (error) {
        console.error('Error fetching decks:', error);
        throw error;
    }
};