import pandas as pd
from modelUtility import calculate_past3
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from fastai.tabular.all import *
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('/kaggle/input/ufc_fights_3yrs_from_7_8_23.csv')

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

X = data[data.columns[8:]]
y = data['fight_duration']