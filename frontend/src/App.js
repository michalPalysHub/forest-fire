import React, {useEffect, useState} from 'react';
import Board from './components/Board'
import styled from 'styled-components';

import Button from 'react-bootstrap/Button';
import Jumbotron from 'react-bootstrap/Jumbotron';
import Table from 'react-bootstrap/Table';
import { RangeStepInput } from 'react-range-step-input';
import './App.css';
import { Container } from 'react-bootstrap';

const StyledLabel = styled.p`
  font-size: 40px;
  text-align: center;
  font-weight: bold;
`;

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

    // String zawierający informację o aktualnym czasie.
    const [dateTime, setDateTime] = useState(null);

    // Indeks sektora wybranego do podglądu parametrów 
    const [selectedSectorIndex, setSelectedSectorIndex] = useState(-1);

    // Częstotliwość pobierania danych z /simulation, szybkość symulacji - zmieniana suwakiem
    const [timeout, setTimeout] = useState(1000);

    // Pobranie danych symulacji dla wszystkich sektorów
    const getSimulationDataFromApi = () => {
        fetch('/sectors')
            .then(response => response.json())
            .then(message => {
                setSectorsData(message['sectors_data'])
                if (message['simulation_run'] === false) {
                    handleStopClick();
                }
            });
    }

    // Pobranie informacji o czasie
    const fetchDateTime = () => {
        setInterval( () => {
            fetch('/datetime')
              .then(response => response.json())
              .then(message => {
                  setDateTime(message['dateTime'])
                  console.log(message['dateTime'])
          })
        }, 250)
    }

    useEffect(() => {
        fetchDateTime()
    }, [])

    // Zmiana statusu określenia 
    const onForestTypeSpecification = () => {
        setDidSpecifyForestType(true);
    }

    // Zmiana statusu inicjalizacji danych w API
    const onDataInit = () => {
        setDidInit(true);
        postDataToAPI({ 'newLoopTime': timeout }, '/settings');
        getSimulationDataFromApi();
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
        setTimeout(1000);
        clearInterval(timer);
        postDataToAPI('Data reset', '/reset');
        postDataToAPI({ 'firefighters_limit': 5 }, '/settings');
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
    let buttonPanel, startStopSimBtn, statsPanel;
    if (didInit === true && didSpecifyForestType === true) {
        if (simulationRun) {
            startStopSimBtn = <Button variant="info" onClick={handleStopClick} style={{ marginRight: '10px' }}>Stop</Button>
        } else {
            startStopSimBtn = <Button variant="info" onClick={handleStartClick} style={{ marginRight: '10px' }}>Start</Button>
        }

        // Panel z przyciskami Start/Stop oraz Reset
        buttonPanel = <div style={{ marginBottom: '5px' }}>
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

        // Panel ze statystykami dla wybranego sektora
        let selectedSectorStats;
        if (sectorsData[selectedSectorIndex] != null) {
            selectedSectorStats = [
                selectedSectorIndex,
                sectorsData[selectedSectorIndex].i,
                sectorsData[selectedSectorIndex].j,
                sectorsData[selectedSectorIndex].temperature,
                sectorsData[selectedSectorIndex].air_humidity,
                sectorsData[selectedSectorIndex].litter_moisture,
                sectorsData[selectedSectorIndex].co2,
                sectorsData[selectedSectorIndex].pm25,
                sectorsData[selectedSectorIndex].wind_directory,
                sectorsData[selectedSectorIndex].wind_speed,
                sectorsData[selectedSectorIndex].ffdi,
                sectorsData[selectedSectorIndex].sector_state,
            ];
        } else {
            selectedSectorStats = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'];
        }
        statsPanel = <div>
            <Jumbotron>
                <Container>
                    <h5>Dane dla wybranego sektora</h5>
                    <Table striped bordered hover>
                        <thead>
                            <tr>
                                <th>Parametr</th>
                                <th>Wartość</th>
                            </tr>
                        </thead>
                        <tbody>
                            {selectedSectorStats.map((statVal, index) => <tr>
                                <td>{sectorParametersNames[index]}</td>
                                <td>{statVal}</td>
                            </tr>)}
                        </tbody>
                    </Table>
                </Container>
            </Jumbotron>
        </div>
    } else {
        buttonPanel = <div></div>
        statsPanel = <div></div>
    }

    return (
      <>
          {sectorsData && dateTime ? (
            <div className="main">
                <StyledLabel> Forest fire </StyledLabel>
                <StyledLabel>{`${dateTime}`}</StyledLabel>
                <Board
                  simulationData={sectorsData}
                  setSelectedSectorIndex={setSelectedSectorIndex}
                  onForestTypeSpecification={onForestTypeSpecification}
                  didSpecifyForestType={didSpecifyForestType}
                  onDataInit={onDataInit}
                  didInit={didInit}
                  postDataToAPI = {postDataToAPI}
                />
                <div className="centered">
                    {buttonPanel}
                    {statsPanel}
                </div>
            </div>
          ) : (
            <span>Loading...</span>
          )}
      </>
    )
};


const sectorParametersNames = [
    "Identyfikator sektora",
    "Wiersz",
    "Kolumna",
    "Temperatura [°C]",
    "Wilgotność powietrza [%]",
    "Wilgotność ściółki [%]",
    "Stężenie CO2 [ppm]",
    "Stężenie PM2,5 [ug/m3]",
    "Kierunek wiatru",
    "Prędkość wiatru [km/h]",
    "FFDI",
    "Stan sektora"
]

const postDataToAPI = (message, endpoint) => {
    fetch(endpoint, {
        method: 'POST',
        cache: 'no-cache',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(message)
    });
};

export default App;