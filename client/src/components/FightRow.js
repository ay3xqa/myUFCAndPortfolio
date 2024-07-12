import "../pages/CSS/FightRow.css";
// import rose from "../images/NAMAJUNAS_ROSE_L_07-13.png";
// import tracy from "../images/CORTEZ_TRACY_L_09-16.png";
import FightPrediction from "./FightPrediction";

export default function FightRow(props){
    console.log(props)
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
        <FightPrediction/> 
        <hr/>
        </>
    )
}