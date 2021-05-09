import React from 'react';
import Square from './components/square'

import Button from 'react-bootstrap/Button';
import './App.css';

// JSON zawierający dane i, j, forestType dla wszystkich komponentów
const squaresData = {}

const App = () => {
    // Pobranie danych inicjacyjnych z API - endpoint '/dimensions'.
    const Data = GetDataFromAPI('dimensions')
    if (Data === null) { return null }
    console.log(Data)
    const noRows = Data.rows
    const noColumns = Data.columns
    const squareSize = Data.squareSize

    // Utworzenie listy współrzędnych dla kolejnych kwadratów
    // Konieczne w celu przypisania im odpowiednich współrzędnych
    const matrixElementsCoords = [];
    for (let i = 0; i < noRows; i++) {
        for (let j = 0; j < noColumns; j++) {
            const elementCoords = [i, j]
            matrixElementsCoords.push(elementCoords)
        }
    }

    // Funkcja wywołania po każdej zmianie danego komponentu Square
    const onSquareUpdate = (id, i, j, forestType) => {
        squaresData[id] = {
            'i': i,
            'j': j,
            'forestType': forestType,
        }
    }

    return (
        <div className="main">
            <h1 className="centered"> Forest fire </h1>
            <div style={{ display: 'flex', justifyContent: 'center' }}>
                <div style={
                    {
                        display: 'block',
                        height: `${noRows * squareSize}px`,
                        width: `${noColumns * squareSize}px`,
                        backgroundColor: 'white',
                        backgroundImage: 'url(/img/map1.png)',
                        boxShadow: '10px 10px 10px lightgray',
                    }
                }>
                    {matrixElementsCoords.map((coords, i) => (
                        <Square size={squareSize}
                            id={i}
                            i={coords[0]}
                            j={coords[1]}
                            onSquareUpdate={onSquareUpdate}
                            key={i}
                        />
                    ))}
                </div>
            </div>
            <div className="centered" >
                <Button variant="info" onClick={handleStartClick}>Start</Button>
            </div>
        </div>
    );
};

const GetDataFromAPI = (endpoint, timeout = null) => {
    const [data, setData] = React.useState(null)

    React.useEffect(() => {
        function getData() {
            fetch(endpoint)
                .then(response => response.json())
                .then(message => setData(message))
        }
        getData()
        // Jeżeli jakakolwiek wartość timeout jest podana funkcja będzie wywoływana co timeout[ms] czasu.
        if (timeout != null) {
            const interval = setInterval(() => getData(), timeout)
            return () => {
                clearInterval(interval)
            }
        }
    }, [])

    return data
};

const PostDataToAPI = (message, endpoint) => {
    fetch(endpoint, {
        method: 'POST',
        cache: 'no-cache',
        headers: {
            'content_type': 'application/json'
        },
        body: JSON.stringify(message)
    })
};

const handleStartClick = () => {
    PostDataToAPI(squaresData, 'init_data');
}

export default App;