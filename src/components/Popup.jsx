import React, {useState} from "react";

import Button from 'react-bootstrap/Button';

let firefightersLimit = 5;

const Popup = (props) => {
    // const [firefightersLimit, setFirefightersLimit] = useState(5);

    const handleSubmit = () => {
        props.handleClose();
        firefightersLimit = document.getElementById('limitFormValue').value;
        // setFirefightersLimit(limit)
        props.postDataToAPI({ 'firefighters_limit': firefightersLimit }, '/settings');
        console.log(firefightersLimit)
    }

    return (
        <div className="popup-box">
          <div className="box">
            <span className="close-icon" onClick={handleSubmit}>x</span>
              <>
                  <form>
                      <b>Podaj liczbę wozów w wybranej jednostce straży pożarnej:</b>
                      <p></p>
                      <input id='limitFormValue' type='number' defaultValue={firefightersLimit}/>
                  </form>
                  <Button variant="info" onClick={handleSubmit} style={{ marginTop: '10px'}}>Potwierdź</Button>
                </>
          </div>
        </div>
        );
    };

export default Popup;