// Functie om JSON-gegevens te laden
async function loadJSON(file) {
    const response = await fetch(file);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

// Laad de JSON-bestanden
async function loadGameData() {
    try {
        const mainData = await loadJSON('main_data.json');
        const objectsData = await loadJSON('objects_data.json');

        console.log(mainData); // Bekijk de geladen gegevens in de console
        console.log(objectsData); // Bekijk de geladen gegevens in de console

        // Hier kun je de gegevens gebruiken om je spel te initialiseren
        initializeGame(mainData, objectsData);
    } catch (error) {
        console.error('Error loading JSON data:', error);
    }
}

// Functie om het spel te initialiseren
function initializeGame(mainData, objectsData) {
    // Gebruik de geladen gegevens om je spel te configureren
    console.log('Game initialized with the following data:');
    console.log(mainData);
    console.log(objectsData);
}

// Start het laden van de gegevens
loadGameData();
