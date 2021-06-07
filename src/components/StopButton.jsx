import React from 'react';
import Button from 'react-bootstrap/Button';

const StopButton = ({handleStopClick}) => {
    return (
        <Button variant="info" onClick={handleStopClick} style={{ marginRight: '2px' }}>Stop</Button>
    )
}

export default StopButton
