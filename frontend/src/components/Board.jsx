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

    // Flaga oznaczająca, czy stan lasu powinien zostać zaktualizowany globalnie.
    const [updateForestTypeGlobal, setUpdateForestTypeGlobal] = useState(false);

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
    const onSectorUpdate = (id, i, j, forestType, isFireSource) => {
        let tmp = sectorsData;
        tmp[id] = {
            'i': i,
            'j': j,
            'forestType': forestType,
            'isFireSource': isFireSource,
        }
        setSectorsData(tmp);
        if (updateForestTypeGlobal) {
            setUpdateForestTypeGlobal(false);
        }
    }


    // Funkcja umożliwiająca pobranie informacji na temat stanu danego sektora
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
                'Content-Type': 'application/json'
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
        setUpdateForestTypeGlobal(true);
    }

    // Funkcje umożliwiająca zmianę typu lasu dla wszystkich sektorów na liściasty
    const setForestTypeToDeciduousGlobally = () => {
        setForestTypeGlobal(1);
        setUpdateForestTypeGlobal(true);
    }

    // Funkcje umożliwiająca zmianę typu lasu dla wszystkich sektorów na mieszany
    const setForestTypeToMixedGlobally = () => {
        setForestTypeGlobal(2);
        setUpdateForestTypeGlobal(true);
    }

    // Funkcje umożliwiająca zmianę typu lasu dla wszystkich sektorów na iglasty
    const setForestTypeToConiferousGlobally = () => {
        setForestTypeGlobal(3);
        setUpdateForestTypeGlobal(true);
    }

    // Warunkowe wyświetlanie/ukrywanie odpowiednich przycisków
    let controlsPanel;

    if (props.didInit === true && props.didSpecifyForestType === true) {
        controlsPanel = <div></div>;
    } else if (props.didInit === false && props.didSpecifyForestType === true) {
        controlsPanel = <div className="centered" style={{
            display: 'flex',
            justifyContent: 'center',
        }}>
            <Button variant="info" onClick={handleInitClick} style={{ marginRight: '10px' }}>Init fire</Button>
        </div>;
    } else {
        controlsPanel = <div className="centered" style={{
            display: 'flex',
            justifyContent: 'center',
        }}>
            <Button variant="info" onClick={props.onForestTypeSpecification} style={{ marginRight: '10px' }}>Save forest type</Button>
            <div style={{
                height: '38px',
            }}></div>
            <DropdownButton variant="info" title="Set forest type globally">
                <Dropdown.Item as="button" onClick={setForestTypeToNoneGlobally}>
                    None
                </Dropdown.Item>
                <Dropdown.Item as="button" onClick={setForestTypeToDeciduousGlobally}>
                    Deciduous
                </Dropdown.Item>
                <Dropdown.Item as="button" onClick={setForestTypeToMixedGlobally}>
                    Mixed
                </Dropdown.Item>
                <Dropdown.Item as="button" onClick={setForestTypeToConiferousGlobally}>
                    Coniferous
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
                                updateForestTypeGlobal={updateForestTypeGlobal}
                                didInit={props.didInit}
                                didSpecifyForestType={props.didSpecifyForestType}
                                setSelectedSectorIndex={props.setSelectedSectorIndex}
                                postDataToAPI={props.postDataToAPI}
                                firefightersAmount={props.firefightersPositions.filter(id=>id===i).length}
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
