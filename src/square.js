import React from 'react';


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

const Square = (props) => {
    const [color, setColor] = React.useState('lightgreen');

    const squareStyle = {
        outline: 'none',
        height: `${props.width}px`,
        width: `${props.height}px`,
        float: 'left', // kolejne kwadraty nie rozszerzają kontenera, ustawiają się poniżej
        borderRadius: '2px',
        borderWidth: '1px',
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
    if (Data === null) { return null}

    const rows = Data.rows  // m wierszy
    const columns = Data.columns // n kolumn
    const areaHeight = Data.area_height // wysokosc calej planszy
    const areaWidth = Data.area_width // szerokosc calej planszy
    const squareHeight = areaHeight/columns // wysokość kwadratu w px
    const squareWidth = areaWidth/rows // szerokość kwadratu w px

    const noSquares = rows*columns
    console.log(rows, columns)
    console.log(areaHeight, areaWidth)
    console.log(squareHeight, squareWidth)

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
                        display: 'block',
                        height: `${areaHeight}px`,
                        width: `${areaWidth}px`,
                        border: '1px solid',
                        background: 'green',
                        boxShadow: '10px 10px 10px lightgray',
                    }}>
                    {Array(noSquares)
                        .fill()
                        .map((x, i) => (
                            <Square width={squareWidth} height={squareHeight} key={i} />
                        ))}
                </div>
            </div>
        </div>
    );
};


export default App;