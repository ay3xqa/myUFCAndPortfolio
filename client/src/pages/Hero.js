import FightRow from "../components/FightRow";
import React, {useState, useEffect} from 'react';
import axios from 'axios';
// import fightData from '../MainCardData.json';


export default function Hero(){
    const [fightData, setFightData] = useState([])
    useEffect(() => {
        axios.get('https://ufc-picks-api-5897a84a5ddf.herokuapp.com/ufc_main_card')
            .then(response => {
                console.log(response.data)
                setFightData(response.data)
            })
            .catch(error => {
                console.error('Error fetching the main card data', error);
            });
      }, []);

    const fights = fightData.map((fight, index) => {
        return (
            <FightRow
                key={index}
                f1_name={fight.f1_name}
                f2_name={fight.f2_name}
                f1_age={fight.f1_age}
                f2_age={fight.f2_age}
                f1_height={fight.f1_height}
                f2_height={fight.f2_height}
                f1_weight={fight.f1_weight}
                f2_weight={fight.f2_weight}
                f1_reach={fight.f1_reach}
                f2_reach={fight.f2_reach}
                f1_image={fight.f1_image}
                f2_image={fight.f2_image}

                // format={fight.format}
                // over_odds={fight.over_odds}
                // under_odds={fight.under_odds}
                // line={fight.line}
                // format={5}
                // over_odds={"+155"}
                // under_odds={"-140"}
                // line={3.5}

                index={index}
                total={fightData.length}
                f1_rank = {fight.f1_rank}
                f2_rank = {fight.f2_rank}
                f1_record = {fight.f1_record}
                f1_ml = {fight.f1_ml}
                f2_record = {fight.f2_record}
                f2_ml = {fight.f2_ml}
                f1_flag = {fight.f1_flag}
                f2_flag = {fight.f2_flag}
            />
        );
    });

    return (
        <>
        <div className="Hero-container"> 
            {fights}
        </div>
        </>
    )
}