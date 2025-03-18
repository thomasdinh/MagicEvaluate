export const getDecks = async () => {
    const BASE_URL = 'http://localhost:8000/all_decks'; // Update with your FastAPI server URL
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