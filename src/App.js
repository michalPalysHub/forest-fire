import React, { useState } from 'react';
import Square from './components/square'

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

    // Utworzenie listy kwadratów
    const squares = matrixElementsCoords.map((coords, i) => (
        <Square size={squareSize}
            i={coords[0]}
            j={coords[1]}
            key={i}
        />
    ))

    return (
        <div>
            <h1> Forest fire </h1>
            <div style={
                {
                    display: 'flex',
                    justifyContent: 'center',
                }}>
                <div style={
                    {
                        display: 'block',
                        height: `${noRows * squareSize}px`,
                        width: `${noColumns * squareSize}px`,
                        border: '1px solid',
                        background: 'green',
                        boxShadow: '10px 10px 10px lightgray',
                    }
                }>
                    {squares}
                </div>
            </div>
            <button onClick={handleStartClick}>Start</button>
        </div>
    );
};

const GetDataFromAPI = (endpoint, timeout=null) => {
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



const PostDataToAPI = () => {
    const message = { 'message': 'Sent from React frontend :)' }

    fetch('/receive', {
        method: 'POST',
        cache: 'no-cache',
        headers: {
            'content_type': 'application/json'
        },
        body: JSON.stringify(message)
    })
};

const handleStartClick = () => {
    // TODO: w jakiś sposób pozyskiwać i, j, forestType ze state squares i zwracać w JSONie 
    // do API przy pomocy PostDataToAPI. Możliwe, że trzeba gdzieś przechowywać te dane
    // (w jakimś słowniku właśnie??) i dodać w Square funkcję onChange, która updateuje te dane
    // w nadrzędnym komponencie - App.
    PostDataToAPI();
    console.log("Start")
}

export default App;