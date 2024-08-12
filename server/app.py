from flask import Flask, request, jsonify, send_file
import sys
import os
from pathlib import Path
import pathlib
from fastai import *
from fastai.learner import load_learner
from modelUtility import create_new_test_fight, get_model_dataframe
from flask_cors import CORS  # Import CORS
import pandas as pd
import boto3
import botocore
from dotenv import load_dotenv
import importlib.util
from apscheduler.schedulers.background import BackgroundScheduler
from maincardspider import MaincardspiderSpider
from datetime import datetime

import subprocess

from scrapy.crawler import CrawlerRunner

app = Flask(__name__)
CORS(app)
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')

S3_BUCKET = 'ufc-picks-bucket'
MODEL_FILE_KEY = 'tabular.pkl'
DATA_FILE_KEY = 'ufc_fights.csv'
MAP_FILE_KEY = 'fighterMap.py'
TRACK_RECORD_FILE_KEY = 'UFC_Trackrecord.csv'
ODDS_FILE = "Odds.json"

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION
)

def get_s3_file_last_modified(bucket, key):
    try:
        response = s3.head_object(Bucket=bucket, Key=key)
        return response['LastModified']
    except botocore.exceptions.ClientError as e:
        print(f"Error fetching metadata for {key}: {e}")
        return None

def download_file_from_s3(bucket_name, object_key, local_file_path):
    import boto3
    import os

    s3 = boto3.client('s3')
    s3_obj = s3.head_object(Bucket=bucket_name, Key=object_key)
    
    # Get S3 object's last modified time
    s3_last_modified = s3_obj['LastModified'].replace(tzinfo=None)  # Convert to timezone-naive

    if os.path.exists(local_file_path):
        local_last_modified = datetime.fromtimestamp(os.path.getmtime(local_file_path))
    else:
        local_last_modified = datetime.min

    # Compare timestamps
    if s3_last_modified > local_last_modified:
        s3.download_file(bucket_name, object_key, local_file_path)

def setup_files():
    # Download necessary files from S3
    download_file_from_s3(S3_BUCKET, MODEL_FILE_KEY, 'tabular.pkl')
    download_file_from_s3(S3_BUCKET, DATA_FILE_KEY, 'ufc_fights.csv')
    download_file_from_s3(S3_BUCKET, TRACK_RECORD_FILE_KEY, 'UFC_Trackrecord.csv')
    download_file_from_s3(S3_BUCKET, MAP_FILE_KEY, 'fighterMap.py')
    download_file_from_s3(S3_BUCKET, ODDS_FILE, 'Odds.json')

def load_fighter_map(file_path):
    spec = importlib.util.spec_from_file_location("fighter_map", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fighter_map

setup_files()
# Import fighter_map from the downloaded file
fighter_map = load_fighter_map('fighterMap.py')

# Adjust pathlib behavior based on the operating system
temp = pathlib.PosixPath
if sys.platform.startswith('win'):
    # Replace PosixPath with WindowsPath temporarily
    pathlib.PosixPath = pathlib.WindowsPath
    pkl_file_path = pathlib.Path("tabular.pkl")
else:
    # Use PosixPath directly on non-Windows systems
    pkl_file_path = "tabular.pkl"
learn = load_learner(pkl_file_path)
pathlib.PosixPath = temp


cleaned_data = get_model_dataframe("ufc_fights.csv")

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


@app.route('/get-trackrecord', methods=['GET'])
def get_trackrecord():
    # Load data from the Excel file
    df = pd.read_csv('UFC_Trackrecord.csv')

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Sort the DataFrame by date in ascending order
    df = df.sort_values(by='Date')

    # Calculate cumulative units
    df['Cumulative_Units'] = df['Units'].cumsum()

    # Prepare data for Chart.js
    # Group by event, taking the last cumulative unit for each event
    chart_data = df.groupby('Event').agg({
        'Cumulative_Units': 'last',
        'Date': 'first'
    }).reset_index()

    # Sort the final DataFrame by the date of the first occurrence of each event
    chart_data = chart_data.sort_values(by='Date')

    # Convert the final DataFrame to a list of dictionaries
    chart_data_list = chart_data.to_dict(orient='records')

    return jsonify(chart_data_list)

@app.route('/get-event-trackrecord', methods=['GET'])
def get_event_details():
    event_name = request.args.get('event')
    if not event_name:
        return jsonify({'error': 'Event name is required'}), 400
    
    # Load data from the CSV file
    try:
        df = pd.read_csv('UFC_Trackrecord.csv', parse_dates=['Date'])
    except FileNotFoundError:
        return jsonify({'error': 'Data file not found'}), 500
    except pd.errors.EmptyDataError:
        return jsonify({'error': 'No data in file'}), 500
    
    # Filter data by event name
    event_data = df[df['Event'] == event_name]
    if event_data.empty:
        return jsonify({'error': 'Event not found'}), 404
    
    # Format the date
    event_date = event_data["Date"].iloc[0]
    formatted_date = event_date.strftime('%m-%d-%Y')

    # Calculate wins and losses
    wins = (event_data['Units'] > 0).sum()
    losses = (event_data['Units'] < 0).sum()

    # Calculate cumulative units
    cumulative_units = event_data['Units'].sum()

    event_details = {
        'event': event_name,
        'date': formatted_date,
        'wins': int(wins),
        'losses': int(losses),
        'cumulative_units': float(round(cumulative_units, 2))
    }
    print(event_details)

    return jsonify(event_details)

@app.route('/ufc_main_card', methods=['GET'])
def get_ufc_main_card():
    return send_file('ufc_main_card.json', mimetype='application/json')

@app.route('/odds_data', methods=['GET'])
def get_odds_file():
    return send_file('Odds.json', mimetype='application/json')

@app.route('/', methods=['GET'])
def home():
    return 'Welcome to the Flask API'

def run_scrapy_spider():
    subprocess.run([sys.executable, 'run_spider.py'], check=True)

def periodic_file_check():
    setup_files()

scheduler = BackgroundScheduler()
scheduler.add_job(periodic_file_check, 'interval', hours=24)  # Check every 24 hours
scheduler.add_job(run_scrapy_spider, 'cron', day_of_week='wed', hour=2, minute=0)
scheduler.start()

if __name__ == '__main__':
    # For local development
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

# For deployment on Heroku
if 'DYNO' in os.environ:
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

