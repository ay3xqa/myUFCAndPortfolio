from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load your trained model
model = joblib.load('path_to_your_model.pkl')

def predict(input_data):
    # Process input_data (if necessary)
    prediction = model.predict(input_data)
    return prediction

@app.route('/predict', methods=['POST'])
def get_prediction():
    data = request.get_json()
    prediction = predict(data)
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)