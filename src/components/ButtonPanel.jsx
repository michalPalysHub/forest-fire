import React from 'react';

const ButtonPanel = () => {
    return (
        <div style={{ marginBottom: '5px' }}>
        <StartStopButton
          simulationRun={simulationRun}
          handleStart={handleStartClick}
          handleStop={handleStopClick}
        />
        <Button variant="info" onClick={handleResetClick}>
          Reset
        </Button>
        <SpeedInput
          simulationRun={simulationRun}
          timeout={timeout}
          onTimeoutSliderChange={onTimeoutSliderChange}
        />
      </div>
    )
}

export default ButtonPanel
