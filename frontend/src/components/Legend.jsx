import React from 'react'
import './Legend.css';

const legendColumnStyle = {
    width: "33.3%",
    height: "100%",
    display: "flex", 
    flexDirection: "column"
}

const LegendButton = ({backgroundColor}) => {
    return <button style={{ outline: "none", height: "30px", width: "30px", borderRadius: "1px", borderWidth: "3px", borderColor: "rgb(63, 213, 76)", opacity: "0.6", background: backgroundColor }}><p className="sc-bdvvtL kZQeGj"></p></button>
}

const Legend = ({ width }) => {
    return (
        <div id='legend' style={{
            width,
            height: "15rem",
            display: "flex",
            marginBottom: "15px",
            borderRadius: "15px",
            backgroundColor: "#cecece",
        }}>
            <div style={legendColumnStyle}>
                <p style={{alignSelf: "center"}}>Typ</p>
                <table>
                    <tbody>
                        <tr>
                            <td>
                                <LegendButton backgroundColor={"red"}></LegendButton>
                            </td>
                            <td>
                                cos tam
                            </td>
                        </tr>
                        <tr>
                            <td>
                            <LegendButton backgroundColor={"aqua"}></LegendButton>
                            </td>
                            <td>
                                coś tam
                            </td>
                        </tr>
                    </tbody>

                </table>
            </div>
            <div style={legendColumnStyle}>
            <p style={{alignSelf: "center"}}>Typ</p>
                <table>
                    <tbody>
                        <tr>
                            <td>
                                <LegendButton></LegendButton>
                            </td>
                            <td>
                                cos tam
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <LegendButton></LegendButton>
                            </td>
                            <td>
                                coś tam
                            </td>
                        </tr>
                    </tbody>

                </table>
            </div>
            <div style={legendColumnStyle}>
            <p style={{alignSelf: "center"}}>Typ</p>
                <table>
                    <tbody>
                        <tr>
                            <td>
                                <LegendButton></LegendButton>
                            </td>
                            <td>
                                cos tam
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <LegendButton></LegendButton>
                            </td>
                            <td>
                                coś tam
                            </td>
                        </tr>
                    </tbody>

                </table>
            </div>
        </div>
    )
}

export default Legend