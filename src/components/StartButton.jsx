import React from 'react';
import Button from 'react-bootstrap/Button';

const StartButton = ({handleStartClick}) => {
    return (
        <Button variant="info" onClick={handleStartClick} style={{ marginRight: '2px' }}>Start</Button>
    )
}

export default StartButton
