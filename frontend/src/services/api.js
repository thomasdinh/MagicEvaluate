const BASE_URL = "http://localhost:8000/"


export const getDecks = async () => {
    const response = await fetch(`${BASE_URL}?q=${encodeURIComponent("all_decks")}`);

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data

    // Check if data and data.data are defined and not empty
    /*if (data && data.data && data.data.length > 0) {
        return data.data[0]; // Return the first card object
    } else {
        throw new Error('No cards found matching the query.');
    }*/
};