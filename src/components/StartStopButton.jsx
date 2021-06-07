import React from 'react';
import StartButton from './StartButton';
import StopButton from './StopButton';

const StartStopButton = ({simulationRun, handleStart, handleStop}) => {
    return (
        <div> 
            {simulationRun ? <StopButton handleStopClick={handleStop}/> : <StartButton handleStartClick={handleStart}/>}
        </div>
    )
}

export default StartStopButton
