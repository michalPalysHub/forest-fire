import React, { useState, useEffect } from 'react';
import Sector from './Sector.jsx'

import Button from 'react-bootstrap/Button';
import '../App.css';

const Board = (props) => {
    // JSON zawierający dane i, j, forestType dla wszystkich komponentów
    const [sectorsData, setSectorsData] = useState({});

    // Pobranie danych inicjacyjnych z API - endpoint '/dimensions'.
    const boardDimensions = GetDataFromAPI('/dimensions')
    if (boardDimensions === null) return null;
    const noRows = boardDimensions.rows
    const noColumns = boardDimensions.columns
    const sectorSize = boardDimensions.sectorSize

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
                return {};
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
        });
    }

    // Warunkowe wyświetlanie/ukrywanie odpowiednich przycisków
    let buttonPanel;
    if (props.didInit === true) {
        buttonPanel = <div></div>;
    } else {
        buttonPanel = <div className="centered" >
            <Button variant="info" onClick={handleInitClick}>Init data</Button>
        </div>;
    }

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'center',}}>
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
                            sectorState={getSectorState(i)}
                            onSectorUpdate={onSectorUpdate}
                            didInit={props.didInit}
                            key={i}
                        />
                    ))}
                </div>
            </div>
            {buttonPanel}
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
