import React from 'react';
import { RangeStepInput } from 'react-range-step-input';

const SpeedInput = ({simulationRun, timeout, onTimeoutSliderChange}) => {

    return (
        <div>
            <p style={{ marginTop: '5px' }}>Prędkość symulacji: {timeout} [ms]</p>
            <RangeStepInput
                min={100} max={3000}
                style={simulationRun ? { pointerEvents: "none", opacity: "0.4" } : {}}
                value={timeout} step={50}
                onChange={onTimeoutSliderChange}
            />
        </div>
    )
}

export default SpeedInput
