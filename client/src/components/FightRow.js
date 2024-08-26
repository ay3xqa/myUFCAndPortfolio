import "../pages/CSS/FightRow.css";
import "../pages/CSS/FightPrediction.css";
import odds from '../Odds.json';

import React, {useState, useEffect} from 'react';
import axios from 'axios';



export default function FightRow(props){
    
    const [apiResponse, setApiResponse] = useState('');
    const [status, setStatus] = useState('loading'); // 'loading', 'success', 'debut_fighter', 'error'

    useEffect(() => {
        const payload = {
            f1_name: props.f1_name,
            f2_name: props.f2_name,
            fight_format: odds[props.index].format
        };

        axios.post('https://ufc-picks-api-5897a84a5ddf.herokuapp.com/predict', payload)
            .then(response => {
                console.log(response.data); // Handle response data
                if (response.data.status === 'success') {
                    setApiResponse(response.data.predicted_duration);
                    setStatus('success');
                } else if (response.data.status === 'debut_fighter') {
                    setStatus('debut_fighter');
                } else {
                    setStatus('error');
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error); // Handle errors
                setStatus('error')
            });
    }, [props.f1_name, props.f2_name, props.index]); // Add dependencies to re-fetch if props change
    return (
        <>
        <div className="FightRow-container">
            <div className = "FightRow-title-container">
                {/* <img className="FightRow-fighter-image" src={require(`../images/${props.f1_image}`)} alt=""></img> */}
                <img className="FightRow-fighter-image" src={props.f1_image} alt=""></img>
                <div className="FightRow-name-container">
                    <div className="FightRow-name">
                        <span className="FightRow-first-name">
                            {props.f1_rank && (
                                <span className={`FightRow-rank ${props.f1_rank.includes('C') ? 'champion' : ''}`}>
                                    {props.f1_rank}
                                </span>
                            )}
                            {props.f1_name.split(' ')[0]}
      
                        </span>
                        <span className="FightRow-last-name">{props.f1_name.split(' ').slice(1).join(' ')}</span>
                    </div>
                </div>
                <div className="FightRow-fighter-info">
                    <img className="FightRow-country" src = {props.f1_flag} alt=""></img>
                    <span>{props.f1_record}</span>
                    <span>{props.f1_ml}</span>
                </div>
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
            <div className = "FightRow-title-container">
                {/* <img className="FightRow-fighter-image" src={require(`../images/${props.f2_image}`)} alt=""></img> */}
                <img className="FightRow-fighter-image" src={props.f2_image} alt=""></img>
                <div className="FightRow-name-container">
                    <div className="FightRow-name">
                        <span className="FightRow-first-name">
                            {props.f2_rank && (
                                <span className={`FightRow-rank ${props.f2_rank.includes('C') ? 'champion' : ''}`}>
                                    {props.f2_rank}
                                </span>
                            )}
                            {props.f2_name.split(' ')[0]}
      
                        </span>
                        <span className="FightRow-last-name">{props.f2_name.split(' ').slice(1).join(' ')}</span>
                    </div>
                </div>
                <div className="FightRow-fighter-info">
                    <img className="FightRow-country" src = {props.f2_flag} alt=""></img>
                    <span>{props.f2_record}</span>
                    <span>{props.f2_ml}</span>
                </div>
            </div>
        </div>
        <div className="FightPrediction-container">
            <span className="FightPrediction-container-rounds">{odds[props.index].format} rounds</span>
            <div className="scoreboard">
                {Array.from({ length: odds[props.index].format }, (_, index) => {
                    const isHighlighted = index < Math.floor(odds[props.index].line);
                    const isPartial = Math.floor(odds[props.index].line) === index;
                    return (
                        <div
                            key={index}
                            className={`round-box ${isHighlighted ? 'highlighted' : ''} ${isPartial ? 'partial' : ''}`}
                        ></div>
                    );
                })}
            </div>
            <div className="Lines">
                <div className={apiResponse ? (apiResponse > (odds[props.index].line*300) ? `Line-container line-highlight` : `Line-container`) : 'Line-container'}>  <span>Over {odds[props.index].line} <br></br> {odds[props.index].over_odds}</span></div>
                <div className={apiResponse ? (apiResponse > (odds[props.index].line*300) ? `Line-container` : `Line-container line-highlight`) : 'Line-container'}>            <span>Under {odds[props.index].line} <br></br>{odds[props.index].under_odds}</span></div>
            </div>
            {(status === "success" || status === "loading")  && <h2>{apiResponse ? (apiResponse > (odds[props.index].line*300) ? `Over ${odds[props.index].line} rounds` : `Under ${odds[props.index].line} rounds`) : 'Calculating...'}</h2>}
            {(status === "success" || status === "loading") && <span>Predicted Duration: {apiResponse ? `${Math.round(apiResponse)} seconds` : 'Calculating...'} </span>}
            {status === "debut_fighter" && <h2>Debut Fighter(s) - No Predictions</h2>}
        </div>
        {props.index < props.total - 1 && <hr className="FightRow-divider"/>}
        </>
    )
}