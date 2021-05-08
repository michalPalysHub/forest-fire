import React from 'react';


const GetDataFromAPI = () => {
    const [data, setData] = React.useState(null)

    React.useEffect(() => {
        fetch('/send')
            .then(response => response.json())
            .then(message => {
                setData(message)
            })
    }, [])

    return data
};

const PostDataToAPI = () => {
    const message = {'message': 'Sent from React frontend :)'}

    fetch('/receive', {
        method: 'POST',
        cache: 'no-cache',
        headers: {
            'content_type':'application/json'
        },
        body: JSON.stringify(message)
    })
};

const Square = (props) => {
    const [color, setColor] = React.useState('lightgreen');

    const squareStyle = {
        outline: 'none',
        height: `${props.size}px`,
        width: `${props.size}px`,
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
    PostDataToAPI()

    const rows = Data.rows  // m wierszy
    const columns = Data.columns // n kolumn
    const squareSize = Data.squareSize
    const areaHeight = rows * squareSize // wysokosc calej planszy
    const areaWidth = columns * squareSize // szerokosc calej planszy

    const noSquares = rows*columns

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
                            <Square size={squareSize} key={i} />
                        ))}
                </div>
            </div>
        </div>
    );
};


export default App;