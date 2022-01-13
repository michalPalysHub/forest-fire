import React from 'react'
//import './Legend.css';

const legendColumnStyle = {
    width: "33.3%",
    height: "100%",
    display: "flex",
    flexDirection: "column"
}

const LegendButton = ({ backgroundColor, borderColors }) => {
    return <button style={{ outline: "none", height: "30px", width: "30px", borderRadius: "1px", borderWidth: "3px", borderColor: borderColors, opacity: "0.6", background: backgroundColor }}><p className="sc-bdvvtL kZQeGj"></p></button>
}

const Legend = ({ width }) => {
    return (
        <div id='legend' style={{
            width,
            height: "19rem",
            display: "flex",
            marginBottom: "15px",
            borderRadius: "15px",
            backgroundColor: "#cecece",
            padding: "15px"
        }}>
            <div style={legendColumnStyle}>
                <p style={{ alignSelf: "center" }}>Type of the forest</p>
                <table>
                    <tbody>
                        <tr>
                            <td class="sector" style={{ width: "40px" }}>
                                <LegendButton backgroundColor={"rgb(192, 192, 192)"} borderColors={"rgb(192, 192, 192)"}></LegendButton>
                            </td>
                            <td>
                                - none
                            </td>
                        </tr>
                        <tr>
                            <td class="sector" style={{ width: "40px" }}>
                                <LegendButton backgroundColor={"#3fd54c"} borderColors={"#3fd54c"}></LegendButton>
                            </td>
                            <td>
                                - deciduous
                            </td>
                        </tr>
                        <tr>
                            <td class="sector" style={{ width: "40px" }}>
                                <LegendButton backgroundColor={"#2a9024"} borderColors={"#2a9024"}></LegendButton>
                            </td>
                            <td>
                                - mixed
                            </td>
                        </tr>
                        <tr>
                            <td class="sector" style={{ width: "40px" }}>
                                <LegendButton backgroundColor={"#1e491d"} borderColors={"#1e491d"}></LegendButton>
                            </td>
                            <td>
                                - coniferous
                            </td>
                        </tr>
                        <hr></hr>
                        <tr>
                            <td class="sector" style={{ width: "40px" }}>
                                <LegendButton backgroundColor={"#cecece"} borderColors={"red"}></LegendButton>
                            </td>
                            <td>
                                - source of the fire
                            </td>
                        </tr>
                        <tr>
                            <td class="sector" style={{ width: "40px" }}>
                                <LegendButton backgroundColor={"rgb(0, 40, 167)"} borderColors={"rgb(0, 40, 167)"}></LegendButton>
                            </td>
                            <td>
                                - fire-station
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div style={legendColumnStyle}>
                <p style={{ alignSelf: "center" }}>Fire threat level</p>
                <table>
                    <tbody>
                        <tr>
                            <td class="sector" style={{ width: "40px" }}>
                                <LegendButton backgroundColor={"#00ff22"} borderColors={"#3fd54c"}></LegendButton>
                            </td>
                            <td>
                                - low
                            </td>
                        </tr>
                        <tr>
                            <td class="sector" style={{ width: "40px" }}>
                                <LegendButton backgroundColor={"#73c205"} borderColors={"#3fd54c"}></LegendButton>
                            </td>
                            <td>
                                - moderate
                            </td>
                        </tr>
                        <tr>
                            <td class="sector" style={{ width: "40px" }}>
                                <LegendButton backgroundColor={"#efe309"} borderColors={"#3fd54c"}></LegendButton>
                            </td>
                            <td>
                                - high
                            </td>
                        </tr>
                        <tr>
                            <td class="sector" style={{ width: "40px" }}>
                                <LegendButton backgroundColor={"#f08808"} borderColors={"#3fd54c"}></LegendButton>
                            </td>
                            <td>
                                - very high
                            </td>
                        </tr>
                        <tr>
                            <td class="sector" style={{ width: "40px" }}>
                                <LegendButton backgroundColor={"#af3a04"} borderColors={"#3fd54c"}></LegendButton>
                            </td>
                            <td>
                                - extremely high
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div style={legendColumnStyle}>
                <p style={{ alignSelf: "center" }}>Fire level</p>
                <table>
                    <tbody>
                        <tr>
                            <td class="sector" style={{ width: "40px" }}>
                                <LegendButton backgroundColor={"#de0000"} borderColors={"#3fd54c"}></LegendButton>
                            </td>
                            <td>
                                - easy to control
                            </td>
                        </tr>
                        <tr>
                            <td class="sector" style={{ width: "40px" }}>
                                <LegendButton backgroundColor={"#6c0000"} borderColors={"#3fd54c"}></LegendButton>
                            </td>
                            <td>
                                - difficult but manageable
                            </td>
                        </tr>
                        <tr>
                            <td class="sector" style={{ width: "40px" }}>
                                <LegendButton backgroundColor={"#4c0000"} borderColors={"#3fd54c"}></LegendButton>
                            </td>
                            <td>
                                - impossible to control
                            </td>
                        </tr>
                        <tr>
                            <td class="sector" style={{ width: "40px" }}>
                                <LegendButton backgroundColor={"#000000"} borderColors={"#3fd54c"}></LegendButton>
                            </td>
                            <td>
                                - burned
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    )
}

export default Legend