import React, { useState, useEffect } from 'react';
import Board from './components/Board'

import Button from 'react-bootstrap/Button';
import './App.css';

const App = () => {
<<<<<<< HEAD
    // Pobranie danych inicjacyjnych z API - endpoint '/dimensions'.
    const Data = GetDataFromAPI('dimensions')
    if (Data === null) { return null }
    console.log(Data)
    const noRows = Data.rows
    const noColumns = Data.columns
    const sectorSize = Data.sectorSize

    // Utworzenie listy współrzędnych dla kolejnych kwadratów
    // Konieczne w celu przypisania im odpowiednich współrzędnych
    const matrixElementsCoords = [];
    for (let i = 0; i < noRows; i++) {
        for (let j = 0; j < noColumns; j++) {
            const elementCoords = [i, j]
            matrixElementsCoords.push(elementCoords)
        }
=======
    // Flaga informująca o tym, czy dane inicjalizacyjne zostały poprawnie odebrane przez API
    const [didInit, setDidInit] = useState(false);

    // JSON zawierający odświeżone dane symulacji pochodzące z API 
    const [simulationData, setSimulationData] = useState({});

    const getSimulationDataFromApi = () => {
        fetch('/simulation')
            .then(response => response.json())
            .then(message => setSimulationData(message));
>>>>>>> d0a0060 (dodano obsługę przycisków oraz Board.js)
    }

    let interval;

    // Uruchomienie symulacji
    const handleStartClick = () => {
        interval = setInterval(() => getSimulationDataFromApi(), 500)
    }

<<<<<<< HEAD
    return (
        <div className="main">
            <h1 className="centered"> Forest fire </h1>
            <div style={{ display: 'flex', justifyContent: 'center' }}>
                <div style={
                    {
                        display: 'block',
                        height: `${noRows * sectorSize}px`,
                        width: `${noColumns * sectorSize}px`,
                        backgroundColor: 'white',
                        backgroundImage: 'url(/img/map1.png)',
                        boxShadow: '10px 10px 10px lightgray',
                    }
                }>
                    {matrixElementsCoords.map((coords, i) => (
                        <Sector size={sectorSize}
                            id={i}
                            i={coords[0]}
                            j={coords[1]}
                            onSectorUpdate={onSectorUpdate}
                            key={i}
                        />
                    ))}
                </div>
            </div>
            <div className="centered" >
                <Button variant="info" onClick={handleStartClick}>Start</Button>
=======
    // Zresetowanie symulacji
    const handleResetClick = () => {
        setDidInit(false);
        clearInterval(interval);
        // TODO: resetuje timer
        // postDataToAPI('Data reset', '/reset');
    }

    // Zmiana statusu inicjalizacji danych w API
    const onDataInit = () => {
        setDidInit(true);
    }

    // Warunkowe wyświetlanie/ukrywanie odpowiednich przycisków
    let buttonPanel;
    if (didInit === true) {
        buttonPanel = <div>
            <Button variant="info" onClick={handleStartClick} style={{ marginRight: '2px' }}>Start</Button>
            <Button variant="info" onClick={handleResetClick}>Reset</Button>
        </div>
    } else {
        buttonPanel = <div></div>
    }

    return (
        <div className="main">
            <h1 className="centered"> Forest fire </h1>
            <Board onDataInit={onDataInit} didInit={didInit} simulationData={simulationData} />
            <div className="centered" >
                {buttonPanel}
>>>>>>> d0a0060 (dodano obsługę przycisków oraz Board.js)
            </div>
        </div>
    );
};

const GetDataFromAPI = (endpoint) => {
    const [data, setData] = useState(null)

    useEffect(() => {
        fetch(endpoint)
            .then(response => response.json())
            .then(message => setData(message))
    }, [])

    return data
};

<<<<<<< HEAD
const PostDataToAPI = (message, endpoint) => {
    fetch(endpoint, {
        method: 'POST',
        cache: 'no-cache',
        headers: {
            'content_type': 'application/json'
        },
        body: JSON.stringify(message)
    })
};

const handleStartClick = () => {
    PostDataToAPI(sectorsData, 'init_data');
}
=======
// simulationData = GetDataFromAPI('/simulation', 2000)
//if ( simulationData === null) { return null }

// const postDataToAPI = (message, endpoint) => {
//     fetch(endpoint, {
//         method: 'POST',
//         cache: 'no-cache',
//         headers: {
//             'content_type': 'application/json'
//         },
//         body: JSON.stringify(message)
//     });
// };
>>>>>>> d0a0060 (dodano obsługę przycisków oraz Board.js)

export default App;