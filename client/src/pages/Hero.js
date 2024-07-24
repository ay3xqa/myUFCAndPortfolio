import FightRow from "../components/FightRow";
import React from 'react';
import fightData from '../MainCardData.json';


export default function Hero(){
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
                format={fight.format}
                over_odds={fight.over_odds}
                under_odds={fight.under_odds}
                line={fight.line}
                index={index}
                total={fightData.length}
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