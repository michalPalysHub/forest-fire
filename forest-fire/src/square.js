import React from 'react';

const n = 10; // ilość wierszy
const m = 10; // ilość kolumn

const Square = () => {
    const [color, setColor] = React.useState('lightgreen');
    const squareStyle = {
        outline: 'none',
        height: '100px',
        width: '100px',
        float: 'left', // kolejne kwadraty nie rozszerzają kontenera, ustawiają się poniżej
        borderRadius: '10px',
        background: `${color}`, // handleClick zmienia stan z useState i tym samnym kolor tutaj
    };

    const handleClick = () => {
        if (color == 'lightgreen') {
            setColor('red');
        } else {
            setColor('lightgreen');
        }
    };

    return <button style={squareStyle} onClick={handleClick}></button>
};

const App = () => {
    const noSquares = n * m;
    return (
        <div>
            <h1>Forest fire</h1>
            <div
                style={{
                    display: 'table',
                    height: '1000px', // 10 wierszy
                    width: '1000px', // 10 kolumn
                    border: '1px solid',
                    background: 'green',
                    boxShadow: '10px 10px 10px lightgray',
                }}>
                {Array(noSquares)
                    .fill()
                    .map((x, i) => (
                        <Square key={i} />
                    ))}
            </div>
        </div>
    );
};


export default App;