import React from 'react';
import Sector from './components/sector'

import Button from 'react-bootstrap/Button';
import './App.css';

// JSON zawierający dane i, j, forestType dla wszystkich komponentów
const sectorsData = {}

const App = () => {
    // Pobranie danych inicjacyjnych z API - endpoint '/dimensions'.
    const Data = GetDataFromAPI('dimensions')
    if (Data === null) { return null }
    console.log(Data)
    const noRows = Data.rows
    const noColumns = Data.columns
    const sectorSize = Data.sectorSize

    // Utworzenie listy współrzędnych dla kolejnych kwadratów
    // Konieczne w celu przypisania im odpowiednich współrzędnych
    const matrixElementsCoords = [];
    for (let i = 0; i < noRows; i++) {
        for (let j = 0; j < noColumns; j++) {
            const elementCoords = [i, j]
            matrixElementsCoords.push(elementCoords)
        }
    }

    // Funkcja wywołania po każdej zmianie danego komponentu Sector
    const onSectorUpdate = (id, i, j, forestType) => {
        sectorsData[id] = {
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
                        height: `${noRows * sectorSize}px`,
                        width: `${noColumns * sectorSize}px`,
                        backgroundColor: 'white',
                        backgroundImage: 'url(/img/map1.png)',
                        boxShadow: '10px 10px 10px lightgray',
                    }
                }>
                    {matrixElementsCoords.map((coords, i) => (
                        <Sector size={sectorSize}
                            id={i}
                            i={coords[0]}
                            j={coords[1]}
                            onSectorUpdate={onSectorUpdate}
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
    PostDataToAPI(sectorsData, 'init_data');
}

export default App;