import React, {useState} from "react";

import Button from 'react-bootstrap/Button';

const Popup = (props) => {

    let firefightersAmount = props.firefightersAmount;

    const handleSubmit = () => {
        props.handleClose();
        firefightersAmount = document.getElementById('limitFormValue').value;
        props.postDataToAPI({ 'firefighters_limit': firefightersAmount }, '/settings');
    }

    return (
        <div className="popup-box">
          <div className="box">
            <span className="close-icon" onClick={handleSubmit}>x</span>
              <>
                  <form>
                      <b>Enter the number of cars in the selected fire department:</b>
                      <p></p>
                      <input id='limitFormValue' type='number' defaultValue={firefightersAmount}/>
                  </form>
                  <Button variant="info" onClick={handleSubmit} style={{ marginTop: '10px'}}>Confirm</Button>
                </>
          </div>
        </div>
        );
    };

export default Popup;