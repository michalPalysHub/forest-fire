import React, {useState} from "react";

import Button from 'react-bootstrap/Button';

let firefightersLimit = 5;

const Popup = (props) => {

    const handleSubmit = () => {
        props.handleClose();
        firefightersLimit = document.getElementById('limitFormValue').value;
        props.postDataToAPI({ 'firefighters_limit': firefightersLimit }, '/settings');
    }

    return (
        <div className="popup-box">
          <div className="box">
            <span className="close-icon" onClick={handleSubmit}>x</span>
              <>
                  <form>
                      <b>Enter the number of cars in the selected fire department:</b>
                      <p></p>
                      <input id='limitFormValue' type='number' defaultValue={firefightersLimit}/>
                  </form>
                  <Button variant="info" onClick={handleSubmit} style={{ marginTop: '10px'}}>Confirm</Button>
                </>
          </div>
        </div>
        );
    };

export default Popup;