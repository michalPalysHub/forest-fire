import React, { useState, useEffect } from 'react';

// Słownik umożliwiający reprezentację danego typu lasu określonym kolorem kwadratu
const forestTypeToSectorColorDict = {
    0: '#c0c0c0', // brak
    1: '#3fd54c', // liściasty
    2: '#2a9024', // mieszany
    3: '#1e491d', // iglasty
};

const forestStateToSectorBorderColorDict = {
    0: '#c0c0c0', // Domyślnie brak koloru krawędzi.
    1: '#00ff22', // Zagrożenie niskie.
    2: '#73c205', // Zagrożenie umiarkowane.
    3: '#efe309', // Zagrożenie wysokie.
    4: '#f08808', // Zagrożenie bardzo wysokie.
    5: '#af3a04', // Zagrożenie ekstremalne.
    6: '#de0000', // Pożar łatwy do opanowania.
    7: '#6c0000', // Pożar trudny, ale możliwy do opanowania.
    8: '#4c0000', // Pożar niemożliwy do opanowania.
    9: '#000000', // Sektor spalony.
}

const fireStationColor = '#0028a7';

// Słownik umożliwiający reprezentację stanu zagrożenia pożarem lub jego zaawansowania dla danego sektora.
const Sector = (props) => {
    // Zmienne stanu reprezentujące współrzędne służące do identyfikacji danego kwadratu
    const [i, setRowIndex] = useState(props.i);
    const [j, setColumnIndex] = useState(props.j);
    const [fireStation, setFireStation] = useState(false);
    const sectorState = props.sectorState;

    // Współrzędne remizy strażackiej.
    const fireStationCoords = {'i': 10, 'j': 28}

    // Oznaczenie flagą sektora, na którym znajduje się remiza straży pożarnej.
    if (i === fireStationCoords['i'] && j === fireStationCoords['j']) {
        if (!fireStation) {
            setFireStation(true);
        }
    }

    // Zmienna określająca typ lasu dla danego sektora
    const [forestType, setForestType] = useState(props.forestTypeGlobal);

    // Zmienna określająca, czy dany sektor jest źródłem (ogniskiem) pożaru
    const [isFireSource, setIsFireSource] = useState(false);

    const updateForestTypeGlobal = () => {
        if (forestType !== props.forestTypeGlobal) {
            setForestType(props.forestTypeGlobal);
        }
    }

    // Funkcja zwracająca kolor sektora.
    const getBackgroundColor = () => {
        if (fireStation) {
            return fireStationColor;
        }
        return props.didInit ? forestStateToSectorBorderColorDict[sectorState] : forestTypeToSectorColorDict[forestType];
    }

    // Funkcja zwracająca kolor granicy sektora.
    const getBorderColor = () => {
        if (fireStation) {
            return fireStationColor;
        }
        return isFireSource ? 'red' : forestTypeToSectorColorDict[forestType];
    }

    // Informacje na temat stylu w CSS
    const sectorStyle = {
        outline: 'none',
        height: `${props.size}px`,
        width: `${props.size}px`,
        float: 'left',
        borderRadius: '1px',
        borderWidth: '3px',
        borderColor: `${getBorderColor()}`,
        opacity: 0.6,
        background: `${getBackgroundColor()}`,
        //pointerEvents: `${props.didInit ? 'none' : 'all'}`,
    };

    // Obsługa kliknięcia
    const handleClick = () => {
        if (props.didInit === false && props.didSpecifyForestType === false && !fireStation) {
            setForestType((forestType + 1) % Object.keys(forestTypeToSectorColorDict).length);
            //forestType = (forestType + 1) % Object.keys(forestTypeToSectorColorDict).length;
        } else if (props.didInit === false && props.didSpecifyForestType === true && !fireStation) {
            setIsFireSource(!isFireSource);
        } else {
            props.setSelectedSectorIndex(props.id);
        }
    };

    // Funkcja wywołania po każdym renderowaniu komponentu (po każdej jego zmianie)
    useEffect(() => {
        props.onSectorUpdate(props.id, i, j, forestType, isFireSource)
        if (props.updateForestTypeGlobal) {
            updateForestTypeGlobal();
        }
    });

    // Zwracany kod HTML
    return <button style={sectorStyle}
        onClick={handleClick}
    />
};

export default Sector;
