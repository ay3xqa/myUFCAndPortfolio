import "../pages/CSS/FightRow.css";
import "../pages/CSS/FightPrediction.css";

// import rose from "../images/NAMAJUNAS_ROSE_L_07-13.png";
// import tracy from "../images/CORTEZ_TRACY_L_09-16.png";
import React, {useState, useEffect} from 'react';
import axios from 'axios';



export default function FightRow(props){
    
    const [apiResponse, setApiResponse] = useState('');

    useEffect(() => {
        const payload = {
            f1_name: props.f1_name,
            f2_name: props.f2_name,
            fight_format: props.format
        };

        axios.post('http://127.0.0.1:5000/predict', payload)
            .then(response => {
                console.log(response.data); // Handle response data
                setApiResponse(response.data.predicted_duration);
            })
            .catch(error => {
                console.error('Error fetching data:', error); // Handle errors
            });
    }, [props.f1_name, props.f2_name, props.format]); // Add dependencies to re-fetch if props change

    return (
        <>
        <div className="FightRow-container">
            <div>
                <img className="FightRow-fighter-image" src={require(`../images/${props.f1_image}`)} alt=""></img>
                <p>{props.f1_name}</p>
            </div>
            <div className="FightRow-statistics">
                <h2>Fight Statistics</h2>
                <ul>
                    <li>
                        <span>{props.f1_age}</span>
                        <p>Age</p>
                        <span>{props.f2_age}</span>
                    </li> 
                    <hr/>
                    <li>
                        <span>{props.f1_height}</span>
                        <p>Height</p>
                        <span>{props.f2_height}</span>
                    </li>
                    <hr/>
                    <li>
                        <span>{props.f1_weight}</span>
                        <p>Weight</p>
                        <span>{props.f2_weight}</span>
                    </li>
                    <hr/>
                    <li>
                        <span>{props.f1_reach}</span>
                        <p>Reach</p>
                        <span>{props.f2_reach}</span>
                    </li>
                </ul>
            </div>
            <div>
                <img className="FightRow-fighter-image" src={require(`../images/${props.f2_image}`)} alt=""></img>
                <p>{props.f2_name}</p>
            </div>
        </div>
        <div className="FightPrediction-container">
            <span>Fight Format: {props.format} rounds</span>
            <span>Over {props.line} {props.over_odds}</span>
            <span>Under {props.line} {props.under_odds}</span>
            <h1>{apiResponse ? (apiResponse > (props.line*300) ? `Over ${props.line} rounds` : `Under ${props.line} rounds`) : 'Calculating...'}</h1>
            <span>Predicted Duration: {apiResponse ? `${apiResponse} seconds` : 'Calculating...'} </span>
        </div>
        {props.index < props.total - 1 && <hr />}
        </>
    )
}