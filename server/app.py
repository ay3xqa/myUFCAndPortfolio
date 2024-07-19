from flask import Flask, request, jsonify
import sys
import os
from pathlib import Path
import pathlib
from fastai import *
from fastai.learner import load_learner
from modelUtility import create_new_test_fight, get_model_dataframe
from fighterMap_7_19_24 import fighter_map
from flask_cors import CORS  # Import CORS


app = Flask(__name__)
CORS(app)

# Load your trained model
# temp = pathlib.PosixPath
# pathlib.PosixPath = pathlib.WindowsPath

# pkl_file_path = Path("tabular-7-12-24.pkl")
# Load the learner from .pkl file
# learn = load_learner(str(pkl_file_path))

# pathlib.PosixPath = temp

# Adjust pathlib behavior based on the operating system
temp = pathlib.PosixPath
if sys.platform.startswith('win'):
    # Replace PosixPath with WindowsPath temporarily
    pathlib.PosixPath = pathlib.WindowsPath
    pkl_file_path = pathlib.Path("tabular-7-19-24.pkl")
else:
    # Use PosixPath directly on non-Windows systems
    pkl_file_path = "tabular-7-19-24.pkl"
learn = load_learner(pkl_file_path)
pathlib.PosixPath = temp


cleaned_data = get_model_dataframe("ufc_fights_from_3yr_7_19_24.csv")

def predict(input_data):
    # Process input_data (if necessary)
    new_fight = create_new_test_fight(cleaned_data, input_data["f1_name"], input_data["f2_name"], input_data["fight_format"], fighter_map)
    prediction = learn.dls.test_dl(new_fight)
    preds, _ = learn.get_preds(dl=prediction)
    predicted_duration = preds.numpy().flatten()[0]
    x = input_data["f1_name"]
    print(f"{x} Predicted Fight Duration: {predicted_duration} seconds")
    return float(predicted_duration)

@app.route('/predict', methods=['GET', "POST"])
def get_prediction():
    data = request.get_json()
    prediction = predict(data)
    return jsonify({'predicted_duration': prediction})

@app.route('/test', methods=['GET'])
def test_endpoint():
    return 'Hello World'

@app.route('/', methods=['GET'])
def home():
    return 'Welcome to the Flask API'

if __name__ == '__main__':
    # For local development
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

# For deployment on Heroku
if 'DYNO' in os.environ:
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))