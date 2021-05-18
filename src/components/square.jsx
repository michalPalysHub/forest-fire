import React, { useState, useEffect } from 'react';

// Słownik umożliwiający reprezentację danego typu lasu określonym kolorem kwadratu
const forestTypeToSquareColorDict = {
    0: 'white',         // brak
    1: 'lightgreen',    // liściasty
    2: 'forestgreen',   // mieszany
    3: 'darkgreen',     // iglasty
};

const forestStateToSquareBorderColorDict = {
    0: null, // Domyślnie brak koloru krawędzi.
    1: '#0CF228', // Zagrożenie niskie.
    2: '#0E921E', // Zagrożenie umiarkowane.
    3: '#8A920E', // Zagrożenie wysokie.
    4: '#F0B708', // Zagrożenie bardzo wysokie.
    5: '#F09108', // Zagrożenie ekstremalne.
    6: '#FE0101', // Pożar łatwy do opanowania.
    7: '#C50000', // Pożar trudny, ale możliwy do opanowania.
    8: '#830000', // Pożar niemożliwy do opanowania.
    9: '#000000', // Sektor spalony.
}

// Słownik umożliwiający reprezentację stanu zagrożenia pożarem lub jego zaawansowania dla danego sektora.
const Square = (props) => {
    // Zmienne stanu reprezentujące współrzędne służące do identyfikacji danego kwadratu
    const [i, setRowIndex] = useState(props.i);
    const [j, setColumnIndex] = useState(props.j);

    // Zmienna określająca typ lasu dla danego kwadratu
    const [forestType, setForestType] = useState(0)

    // Zmienna przechowująca stan danego sektora.
    const forestState = 0;
    console.log(forestState)

    // Informacje na temat stylu w CSS
    const squareStyle = {
        outline: 'none',
        height: `${props.size}px`,
        width: `${props.size}px`,
        float: 'left', // kolejne kwadraty nie rozszerzają kontenera, ustawiają się poniżej
        borderRadius: '1px',
        borderWidth: '2px',
        borderColor: `${forestStateToSquareBorderColorDict[forestState]}`,
        opacity: 0.6,
        background: `${forestTypeToSquareColorDict[forestType]}`,
    };

    // Obsługa kliknięcia
    const handleClick = () => {
        setForestType((forestType + 1) % Object.keys(forestTypeToSquareColorDict).length)
    };

    // Funkcja wywołania po każdym renderowaniu komponentu (po każdej jego zmianie)
    useEffect(() => {
        props.onSquareUpdate(props.id, i, j, forestType)
    });

    // Zwracany kod HTML
    return <button style={squareStyle}
        onClick={handleClick}
    />
};

export default Square;