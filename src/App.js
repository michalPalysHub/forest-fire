import React, { useState, useEffect } from 'react';
import Board from './components/Board'

import Button from 'react-bootstrap/Button';
import { RangeStepInput } from 'react-range-step-input';
import './App.css';

const App = () => {
    // Flaga informująca o tym, czy został określony obszar lasu oraz jego typ dla wszystkich sektorów
    const [didSpecifyForestType, setDidSpecifyForestType] = useState(false);

    // Flaga informująca o tym, czy dane inicjalizacyjne zostały poprawnie odebrane przez API
    const [didInit, setDidInit] = useState(false);

    // Flaga informująca o tym, czy symulacja jest w trakcie działania
    const [simulationRun, setSimulationRun] = useState(false);

    // Timer służący do uruchamiania/zatrzymywania symulacji
    const [timer, setTimer] = useState(null);

    // JSON zawierający aktualne dane każdego z sektorów pochodzące z API
    const [sectorsData, setSectorsData] = useState({});

    // Częstotliwość pobierania danych z /simulation, szybkość symulacji - zmieniana suwakiem
    const [timeout, setTimeout] = useState(750);

    // Pobranie danych symulacji dla wszystkich sektorów
    const getSimulationDataFromApi = () => {
        fetch('/sectors')
            .then(response => response.json())
            .then(message => {
                setSectorsData(message['sectors'])
                if (message['simulation_run'] === false) {
                    handleStopClick();
                }
            }
            );
    }

    // Zmiana statusu określenia 
    const onForestTypeSpecification = () => {
        setDidSpecifyForestType(true);
    }

    // Zmiana statusu inicjalizacji danych w API
    const onDataInit = () => {
        setDidInit(true);
        getSimulationDataFromApi();
        postDataToAPI({ 'newLoopTime': timeout }, '/settings');
    }

    // Uruchomienie symulacji
    const handleStartClick = () => {
        setSimulationRun(true);
        setTimer(setInterval(() => getSimulationDataFromApi(), timeout));
        postDataToAPI('Start simulation', '/start')
    }

    // Zatrzymanie symulacji
    const handleStopClick = () => {
        setSimulationRun(false);
        clearInterval(timer);
        postDataToAPI('Stop simulation', '/stop');
    }

    // Zresetowanie symulacji
    const handleResetClick = () => {
        setDidInit(false);
        setDidSpecifyForestType(false);
        setSimulationRun(false);
        setTimeout(750);
        clearInterval(timer);
        postDataToAPI('Data reset', '/reset');
        for (var id = 0; id < Object.keys(sectorsData).length; id++) {
            if (sectorsData[id] != null) {
                sectorsData[id].sector_state = 0;
                sectorsData[id].is_fire_source = false;
            }
        }
    }

    // Zmiana częstotliwości pobierania danych z /simulation, szybkości symulacji
    const onTimeoutSliderChange = (e) => {
        const newVal = e.target.value;
        setTimeout(newVal);
        postDataToAPI({ 'newLoopTime': newVal }, '/settings')
    }

    // Warunkowe wyświetlanie/ukrywanie odpowiednich przycisków
    let buttonPanel, startStopSimBtn;
    if (didInit === true && didSpecifyForestType === true) {
        if (simulationRun) {
            startStopSimBtn = <Button variant="info" onClick={handleStopClick} style={{ marginRight: '2px' }}>Stop</Button>
        } else {
            startStopSimBtn = <Button variant="info" onClick={handleStartClick} style={{ marginRight: '2px' }}>Start</Button>
        }
        buttonPanel = <div>
            {startStopSimBtn}
            <Button variant="info" onClick={handleResetClick}>Reset</Button>
            <p style={{ marginTop: '5px' }}>Prędkość symulacji: {timeout} [ms]</p>
            <RangeStepInput
                min={100} max={3000}
                style={simulationRun ? { pointerEvents: "none", opacity: "0.4" } : {}}
                value={timeout} step={50}
                onChange={onTimeoutSliderChange}
            />
        </div>
    } else {
        buttonPanel = <div></div>
    }

    return (
        <div className="main">
            <h1 className="centered"> Forest fire </h1>
            <Board simulationData={sectorsData}
                onForestTypeSpecification={onForestTypeSpecification} didSpecifyForestType={didSpecifyForestType}
                onDataInit={onDataInit} didInit={didInit} />
            <div className="centered">
                {buttonPanel}
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

export default App;