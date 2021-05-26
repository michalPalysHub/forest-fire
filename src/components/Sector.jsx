import React, { useState, useEffect } from 'react';

// Słownik umożliwiający reprezentację danego typu lasu określonym kolorem kwadratu
const forestTypeToSectorColorDict = {
    0: 'white',         // brak
    1: 'lightgreen',    // liściasty
    2: 'forestgreen',   // mieszany
    3: 'darkgreen',     // iglasty
};

const forestStateToSectorBorderColorDict = {
    0: '#C0C0C0', // Domyślnie brak koloru krawędzi.
    1: '#00c21a', // Zagrożenie niskie.
    2: '#73c205', // Zagrożenie umiarkowane.
    3: '#efe309', // Zagrożenie wysokie.
    4: '#f08808', // Zagrożenie bardzo wysokie.
    5: '#af3a04', // Zagrożenie ekstremalne.
    6: '#de0000', // Pożar łatwy do opanowania.
    7: '#6c0000', // Pożar trudny, ale możliwy do opanowania.
    8: '#4c0000', // Pożar niemożliwy do opanowania.
    9: '#000000', // Sektor spalony.
}

// Słownik umożliwiający reprezentację stanu zagrożenia pożarem lub jego zaawansowania dla danego sektora.
const Sector = (props) => {
    // Zmienne stanu reprezentujące współrzędne służące do identyfikacji danego kwadratu
    const [i, setRowIndex] = useState(props.i);
    const [j, setColumnIndex] = useState(props.j);
    const sectorState = props.sectorState

    // Zmienna określająca typ lasu dla danego kwadratu
    const [forestType, setForestType] = useState(_ => {
        if (i < 5 && j < 5) {
            return 1;
        } else {
            return 1;
        }
    })

    // Informacje na temat stylu w CSS
    const sectorStyle = {
        outline: 'none',
        height: `${props.size}px`,
        width: `${props.size}px`,
        float: 'left', // kolejne kwadraty nie rozszerzają kontenera, ustawiają się poniżej
        borderRadius: '1px',
        borderWidth: '3px',
        borderColor: `${forestTypeToSectorColorDict[forestType]}`,
        opacity: 0.6,
        background: `${props.didInit ? forestStateToSectorBorderColorDict[sectorState] : forestTypeToSectorColorDict[forestType]}`,
        pointerEvents: `${props.didInit ? 'none' : 'all'}`,
    };


    // Obsługa kliknięcia
    const handleClick = () => {
        if (props.didInit === false){
            setForestType((forestType + 1) % Object.keys(forestTypeToSectorColorDict).length)
        }
    };

    // Funkcja wywołania po każdym renderowaniu komponentu (po każdej jego zmianie)
    useEffect(() => {
        props.onSectorUpdate(props.id, i, j, forestType)
    });

    // Zwracany kod HTML
    return <button style={sectorStyle}
        onClick={handleClick}
    />
};

export default Sector;