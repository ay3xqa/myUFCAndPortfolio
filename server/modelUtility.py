import pandas as pd
import numpy as np
from datetime import datetime, timedelta

#Return a dictionary of the average fighting stats in the past 3 years for a given fighter
def average_fighting_stats(df, fighter_id):
    # Filter data for rows where fighter1_id or fighter2_id matches fighter_id
    three_years_ago = pd.to_datetime(datetime.now() - timedelta(days=3*365))
    filtered_data = df[(df['fighter1_id'] == fighter_id) | (df['fighter2_id'] == fighter_id) & (df['date'] >= three_years_ago)]
    
    # Select columns containing fighting statistics for averaging
    averages = {}
    averages["_knockdown"] = averages.get("_knockdown", 0) + filtered_data[filtered_data["fighter1_id"]==fighter_id]["f1_knockdown"].sum() + filtered_data[filtered_data["fighter2_id"]==fighter_id]["f2_knockdown"].sum()
    averages["_sig_strike_land"] = averages.get("_sig_strike_land", 0) + filtered_data[filtered_data["fighter1_id"]==fighter_id]["f1_sig_strike_land"].sum() + filtered_data[filtered_data["fighter2_id"]==fighter_id]["f2_sig_strike_land"].sum()
    averages["_sig_strike_att"] = averages.get("_sig_strike_att", 0) + filtered_data[filtered_data["fighter1_id"]==fighter_id]["f1_sig_strike_att"].sum() + filtered_data[filtered_data["fighter2_id"]==fighter_id]["f2_sig_strike_att"].sum()
    averages["_total_strike_land"] = averages.get("_total_strike_land", 0) + filtered_data[filtered_data["fighter1_id"]==fighter_id]["f1_total_strike_land"].sum() + filtered_data[filtered_data["fighter2_id"]==fighter_id]["f2_total_strike_land"].sum()
    averages["_total_strike_att"] = averages.get("_total_strike_att", 0) + filtered_data[filtered_data["fighter1_id"]==fighter_id]["f1_total_strike_att"].sum() + filtered_data[filtered_data["fighter2_id"]==fighter_id]["f2_total_strike_att"].sum()
    averages["_takedown_land"] = averages.get("_takedown_land", 0) + filtered_data[filtered_data["fighter1_id"]==fighter_id]["f1_takedown_land"].sum() + filtered_data[filtered_data["fighter2_id"]==fighter_id]["f2_takedown_land"].sum()
    averages["_takedown_att"] = averages.get("_takedown_att", 0) + filtered_data[filtered_data["fighter1_id"]==fighter_id]["f1_takedown_att"].sum() + filtered_data[filtered_data["fighter2_id"]==fighter_id]["f2_takedown_att"].sum()
    averages["_sub_att"] = averages.get("_sub_att", 0) + filtered_data[filtered_data["fighter1_id"]==fighter_id]["f1_sub_att"].sum() + filtered_data[filtered_data["fighter2_id"]==fighter_id]["f2_sub_att"].sum()
    averages["_reversal"] = averages.get("_reversal", 0) + filtered_data[filtered_data["fighter1_id"]==fighter_id]["f1_reversal"].sum() + filtered_data[filtered_data["fighter2_id"]==fighter_id]["f2_reversal"].sum()
    averages["_control_time"] = averages.get("_control_time", 0) + filtered_data[filtered_data["fighter1_id"]==fighter_id]["f1_control_time"].sum() + filtered_data[filtered_data["fighter2_id"]==fighter_id]["f2_control_time"].sum()
    
    avg_values = {key: value / len(filtered_data) for key, value in averages.items()}
    
    return avg_values

# Function to calculate past 3 fight results for each fighter at that time and compile a score (+1 for win, -1 for loss)
def calculate_past3(row, df):
    fighter1 = row['fighter1']
    fighter2 = row['fighter2']
    
    # Get the index of the current row
    current_index = row.name
    
    # Filter the DataFrame for fights prior to the current row
    past_fights = df.iloc[current_index+1:]
    
    # Filter past fights for each fighter's past 3 fights
    past_fights_fighter1 = past_fights[((past_fights['fighter1'] == fighter1) | (past_fights['fighter2'] == fighter1))].head(3)
    past_fights_fighter2 = past_fights[((past_fights['fighter1'] == fighter2) | (past_fights['fighter2'] == fighter2))].head(3)
    
    # Calculate wins and losses for fighter1 regardless of their position
    fighter1_wins = (((past_fights_fighter1['fighter1'] == fighter1) & (past_fights_fighter1['result'] == 1)) |
                     ((past_fights_fighter1['fighter2'] == fighter1) & (past_fights_fighter1['result'] == 0))).sum()
    
    fighter1_losses = (((past_fights_fighter1['fighter1'] == fighter1) & (past_fights_fighter1['result'] == 0)) |
                       ((past_fights_fighter1['fighter2'] == fighter1) & (past_fights_fighter1['result'] == 1))).sum()
    
    # Calculate wins and losses for fighter2 regardless of their position
    fighter2_wins = (((past_fights_fighter2['fighter1'] == fighter2) & (past_fights_fighter2['result'] == 1)) |
                     ((past_fights_fighter2['fighter2'] == fighter2) & (past_fights_fighter2['result'] == 0))).sum()
    
    fighter2_losses = (((past_fights_fighter2['fighter1'] == fighter2) & (past_fights_fighter2['result'] == 0)) |
                       ((past_fights_fighter2['fighter2'] == fighter2) & (past_fights_fighter2['result'] == 1))).sum()
    
    # Return sum of wins and losses for each fighter
    return pd.Series({
        'fighter1_past3': fighter1_wins - fighter1_losses,
        'fighter2_past3': fighter2_wins - fighter2_losses
    })

#Create a new test point to feed into the model and predict
def create_new_test_fight(df, f1_name, f2_name, num_rounds, fighter_id_map):
    if f1_name not in fighter_id_map or f2_name not in fighter_id_map:
        return None
    f1_id = fighter_id_map[f1_name]
    f2_id = fighter_id_map[f2_name]
    f1_avg_stats = average_fighting_stats(df, f1_id)
    f2_avg_stats = average_fighting_stats(df, f2_id)
    new_fight = pd.DataFrame({"fight_format": [num_rounds]})
    for key in f1_avg_stats:
        new_fight["f1"+key] = f1_avg_stats[key]
        new_fight["f2"+key] = f2_avg_stats[key]
    new_fight["fighter1_id"] = f1_id
    new_fight["fighter2_id"] = f2_id
    past3_values = calculate_past3_new_fight(f1_name, f2_name,df)
    new_fight[['fighter1_past3', 'fighter2_past3']] = pd.DataFrame([past3_values])
    return new_fight

#Calculate the past 3 fight results and compute a score ----- FOR NEW TEST POINT USE ONLY!
def calculate_past3_new_fight(fighter1, fighter2, df):
    past_fights = df
    
    # Filter past fights for each fighter's past 3 fights
    past_fights_fighter1 = past_fights[((past_fights['fighter1'] == fighter1) | (past_fights['fighter2'] == fighter1))].head(3)
    past_fights_fighter2 = past_fights[((past_fights['fighter1'] == fighter2) | (past_fights['fighter2'] == fighter2))].head(3)
    
    # Calculate wins and losses for fighter1 regardless of their position
    fighter1_wins = (((past_fights_fighter1['fighter1'] == fighter1) & (past_fights_fighter1['result'] == 1)) |
                     ((past_fights_fighter1['fighter2'] == fighter1) & (past_fights_fighter1['result'] == 0))).sum()
    
    fighter1_losses = (((past_fights_fighter1['fighter1'] == fighter1) & (past_fights_fighter1['result'] == 0)) |
                       ((past_fights_fighter1['fighter2'] == fighter1) & (past_fights_fighter1['result'] == 1))).sum()
    
    # Calculate wins and losses for fighter2 regardless of their position
    fighter2_wins = (((past_fights_fighter2['fighter1'] == fighter2) & (past_fights_fighter2['result'] == 1)) |
                     ((past_fights_fighter2['fighter2'] == fighter2) & (past_fights_fighter2['result'] == 0))).sum()
    
    fighter2_losses = (((past_fights_fighter2['fighter1'] == fighter2) & (past_fights_fighter2['result'] == 0)) |
                       ((past_fights_fighter2['fighter2'] == fighter2) & (past_fights_fighter2['result'] == 1))).sum()
    
    # Return sum of wins and losses for each fighter
    return pd.Series({
        'fighter1_past3': fighter1_wins - fighter1_losses,
        'fighter2_past3': fighter2_wins - fighter2_losses
    })

def get_model_dataframe(filepath):
    data = pd.read_csv(filepath)
    # Preprocess the data
    data['date'] = pd.to_datetime(data['date'])
    #data = data[data['fight_format'] == 3]

    #sort the df by date
    data.sort_values(by=['date'], ascending=False, inplace=True)
    data = data.reset_index(drop=True)

    #map fighter names to an integer id
    fighter_names = pd.concat([data['fighter1'], data['fighter2']])

    # # Create a mapping of unique fighter names to unique identifiers
    unique_fighters = fighter_names.unique()
    fighter_id_map = {fighter: idx for idx, fighter in enumerate(unique_fighters)}

    # Map fighter names in 'fighter1' and 'fighter2' columns to their respective identifiers
    data['fighter1_id'] = data['fighter1'].map(fighter_id_map)
    data['fighter2_id'] = data['fighter2'].map(fighter_id_map)

    # # Display the mapping of fighter names to their corresponding identifiers
    # print("Fighter Name to ID Mapping:")
    # for fighter, fighter_id in fighter_id_map.items():
    #     print(f"{fighter}: {fighter_id}")

        
    #Create new features which is a score of their past 3 fights
    data[['fighter1_past3', 'fighter2_past3']] = data.apply(lambda row: calculate_past3(row, data), axis=1)
    return data