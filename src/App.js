import React, { useState, useEffect } from 'react';
import Board from './components/Board'

import Button from 'react-bootstrap/Button';
import { RangeStepInput } from 'react-range-step-input';
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

    // Flaga informująca o tym, czy symulacja jest w trakcie działania
    const [simulationRun, setSimulationRun] = useState(false);

    // Timer służący do uruchamiania/zatrzymywania symulacji
    const [timer, setTimer] = useState(null);

    // JSON zawierający aktualne dane symulacji pochodzące z API 
    const [simulationData, setSimulationData] = useState({});

    // Częstotliwość pobierania danych z /simulation, szybkość symulacji - zmieniana suwakiem
    const [timeout, setTimeout] = useState(500);

    const getSimulationDataFromApi = () => {
        fetch('/simulation')
            .then(response => response.json())
            .then(message => setSimulationData(message));
>>>>>>> d0a0060 (dodano obsługę przycisków oraz Board.js)
    }

    // Uruchomienie symulacji
    const handleStartClick = () => {
        setSimulationRun(true);
        setTimer(setInterval(() => getSimulationDataFromApi(), timeout))
    }

    // Zatrzymanie symulacji
    const handleStopClick = () => {
        setSimulationRun(false);
        clearInterval(timer);
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
        setSimulationRun(false);
        clearInterval(timer);
        postDataToAPI('Data reset', '/reset');
        for (var id = 0; id < Object.keys(simulationData).length; id++){
            simulationData[id].sector_state = 0;
        }
    }

    // Zmiana statusu inicjalizacji danych w API
    const onDataInit = () => {
        setDidInit(true);
    }

    // Zmiana częstotliwości pobierania danych z /simulation, szybkości symulacji
    const onTimeoutSliderChange = (e) => {
        const newVal = e.target.value;
        setTimeout(newVal);
    }

    // Warunkowe wyświetlanie/ukrywanie odpowiednich przycisków
    let buttonPanel, startStopSimBtn;
    if (didInit === true) {
        if (simulationRun){
            startStopSimBtn = <Button variant="info" onClick={handleStopClick} style={{ marginRight: '2px' }}>Stop</Button>
        } else {
            startStopSimBtn = <Button variant="info" onClick={handleStartClick} style={{ marginRight: '2px' }}>Start</Button>
        }
        buttonPanel = <div>
            {startStopSimBtn}
            <Button variant="info" onClick={handleResetClick}>Reset</Button>
            <p style={{marginTop: '5px'}}>Szybkość symulacji: {timeout} [ms]</p>
            <RangeStepInput 
                min={100} max={3000}
                style={simulationRun ? {pointerEvents: "none", opacity: "0.4"} : {}}
                value={timeout} step={100}
                onChange={onTimeoutSliderChange}
            />
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

const postDataToAPI = (message, endpoint) => {
    fetch(endpoint, {
        method: 'POST',
        cache: 'no-cache',
        headers: {
            'content_type': 'application/json'
        },
        body: JSON.stringify(message)
    });
};

<<<<<<< HEAD
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

=======
>>>>>>> a527e30 (przyciski Start, Stop, Reset działają teraz poprawnie, dodano suwak do regulacji szybkości symulacji)
export default App;