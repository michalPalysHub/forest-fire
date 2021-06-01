import React, { useState, useEffect } from 'react';
import Sector from './Sector.jsx'

import Button from 'react-bootstrap/Button';
import DropdownButton from 'react-bootstrap/DropdownButton';
import Dropdown from 'react-bootstrap/Dropdown';
import '../App.css';

const Board = (props) => {
    // JSON zawierający dane i, j, forestType dla wszystkich komponentów
    const [sectorsData, setSectorsData] = useState({});

    // Globalnie ustawiony typ lasu
    const [forestTypeGlobal, setForestTypeGlobal] = useState(1);

    // Pobranie danych inicjacyjnych z API - endpoint '/dimensions'.
    const boardDimensions = GetDataFromAPI('/dimensions')
    if (boardDimensions === null) return null;
    const noRows = 20
    const noColumns = 40
    const sectorSize = 30

    // Utworzenie listy współrzędnych dla kolejnych sektorów
    const matrixElementsCoords = [];
    for (let i = 0; i < noRows; i++) {
        for (let j = 0; j < noColumns; j++) {
            const elementCoords = [i, j]
            matrixElementsCoords.push(elementCoords)
        }
    }

    // Funkcja wywoływana po każdej zmianie danego komponentu Sector
    const onSectorUpdate = (id, i, j, forestType) => {
        let tmp = sectorsData;
        tmp[id] = {
            'i': i,
            'j': j,
            'forestType': forestType,
        }
        setSectorsData(tmp);
    }

    // Funkcja zmieniająca obwódkę danego komponentu Sector w zależności od jego stanu
    const getSectorState = (id) => {
        if (props.simulationData) {
            if (id in props.simulationData) {
                return props.simulationData[id].sector_state;
            } else {
                return 0;
            }
        }
    }

    // Inicjalizacja danych
    const handleInitClick = () => {
        fetch('/init_data', {
            method: 'POST',
            cache: 'no-cache',
            headers: {
                'content_type': 'application/json'
            },
            body: JSON.stringify(sectorsData)
        }).then(function (response) {
            if (response.status === 200) {
                props.onDataInit();
            }
        })
    }

    // Funkcje umożliwiająca zmianę typu lasu dla wszystkich sektorów na brak
    const setForestTypeToNoneGlobally = () => {
        setForestTypeGlobal(0);
    }

    // Funkcje umożliwiająca zmianę typu lasu dla wszystkich sektorów na liściasty
    const setForestTypeToDeciduousGlobally = () => {
        setForestTypeGlobal(1);
    }

    // Funkcje umożliwiająca zmianę typu lasu dla wszystkich sektorów na mieszany
    const setForestTypeToMixedGlobally = () => {
        setForestTypeGlobal(2);
    }

    // Funkcje umożliwiająca zmianę typu lasu dla wszystkich sektorów na iglasty
    const setForestTypeToConiferousGlobally = () => {
        setForestTypeGlobal(3);
    }

    // Warunkowe wyświetlanie/ukrywanie odpowiednich przycisków
    let controlsPanel;
    if (props.didInit === true) {
        controlsPanel = <div></div>;
    } else {
        controlsPanel = <div className="centered" style={{
            display: 'flex',
            justifyContent: 'center',
        }}>
            <Button variant="info" onClick={handleInitClick} style={{ marginRight: '10px' }}>Inicjuj</Button>
            <div style={{
                borderLeft: '3px solid black',
                height: '38px',
                marginRight: '10px',
            }}></div>
            <DropdownButton variant="info" title="Ustaw typ lasu globalnie">
                <Dropdown.Item as="button" onClick={setForestTypeToNoneGlobally}>
                    Brak
                </Dropdown.Item>
                <Dropdown.Item as="button" onClick={setForestTypeToDeciduousGlobally}>
                    Liściasty
                </Dropdown.Item>
                <Dropdown.Item as="button" onClick={setForestTypeToMixedGlobally}>
                    Mieszany
                </Dropdown.Item>
                <Dropdown.Item as="button" onClick={setForestTypeToConiferousGlobally}>
                    Iglasty
                </Dropdown.Item>
            </DropdownButton>
        </div>;
    }

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'center', }}>
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
                            forestTypeGlobal={forestTypeGlobal}
                            sectorState={getSectorState(i)}
                            onSectorUpdate={onSectorUpdate}
                            didInit={props.didInit}
                            key={i}
                        />
                    ))}
                </div>
            </div>
            {controlsPanel}
        </div>
    );
}

const GetDataFromAPI = (endpoint) => {
    const [data, setData] = useState(null)

    useEffect(() => {
        fetch(endpoint)
            .then(response => response.json())
            .then(message => setData(message))
    }, [])

    return data
};

export default Board;
