import React, { useState } from 'react';

// Słownik umożliwiający reprezentację danego typu lasu określonym kolorem kwadratu
const forestTypeToSquareColorDict = {
    0: 'white',         // brak
    1: 'lightgreen',    // liściasty
    2: 'forestgreen',   // mieszany
    3: 'darkgreen',     // iglasty
};

const Square = (props) => {
    // Zmienne stanu reprezentujące współrzędne służące do identyfikacji danego kwadratu
    const [i, setRowIndex] = useState(props.i);
    const [j, setColumnIndex] = useState(props.j);

    // Zmienna określająca typ lasu dla danego kwadratu
    const [forestType, setForestType] = useState(0)

    // Informacje na temat stylu w CSS
    const squareStyle = {
        outline: 'none',
        height: `${props.size}px`,
        width: `${props.size}px`,
        float: 'left', // kolejne kwadraty nie rozszerzają kontenera, ustawiają się poniżej
        borderRadius: '2px',
        borderWidth: '1px',
        background: `${forestTypeToSquareColorDict[forestType]}`,
    };

    // Obsługa kliknięcia
    const handleClick = () => {
        setForestType((forestType + 1) % Object.keys(forestTypeToSquareColorDict).length)
        console.log('i:', i, ' j:', j, ' forestType:', forestType) // sprawdzenie
    };

    // Zwracany kod HTML
    return <button style={squareStyle}
        onClick={handleClick}
    />
};

export default Square;