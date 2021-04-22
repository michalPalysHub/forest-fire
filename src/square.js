import React from 'react';


const M = 10 // m wierszy
const N = 10 // n kolumn
const AREA_HEIGHT = 800 // wysokosc calej planszy
const AREA_WIDTH = 800  // szerokosc calej planszy
const SQUARE_HEIGHT = AREA_HEIGHT/N // wysokość kwadratu w px
const SQUARE_WIDTH = AREA_WIDTH/M // szerokość kwadratu w px

const GetDataFromAPI = () => {
    const [data, setData] = React.useState(null)

    React.useEffect(() => {
        fetch('/api')
            .then(response => response.json())
            .then(message => {
                setData(message)
            })
    }, [])

    return data
}

const Square = () => {
    const [color, setColor] = React.useState('lightgreen');
    const squareStyle = {
        outline: 'none',
        height: `${SQUARE_HEIGHT}px`,
        width: `${SQUARE_WIDTH}px`,
        float: 'left', // kolejne kwadraty nie rozszerzają kontenera, ustawiają się poniżej
        borderRadius: '5px',
        background: `${color}`, // handleClick zmienia stan z useState i tym samnym kolor tutaj
    };

    const handleClick = () => {
        if (color === 'lightgreen') {
            setColor('red');
        } else {
            setColor('lightgreen');
        }
    };

    return <button style={squareStyle} onClick={handleClick}/>
};

const App = () => {
    const Data = GetDataFromAPI()
    console.log(Data)

    const noSquares = M*N

    return (
        <div>
            <h1>Forest fire</h1>
            <div
                style={{
                    display: 'flex',
                    justifyContent: 'center',
                }}>
                <div
                    style={{
                        display: 'table',
                        height: `${N * SQUARE_HEIGHT}px`, // n wierszy
                        width: `${M * SQUARE_WIDTH}px`, // m kolumn
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
        </div>
    );
};


export default App;