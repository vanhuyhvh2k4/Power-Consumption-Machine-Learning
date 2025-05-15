from flask import Flask, request, render_template
import joblib
import numpy as np

# Load the model and scaler
model = joblib.load("../Model/random_forest_model.pkl")
scaler = joblib.load("../Model/scaler.pkl")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    try:
        # Get input values from the form
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        windspeed = float(request.form['windspeed'])
        general_diffuse_flows = float(request.form['general_diffuse_flows'])
        hour = int(request.form['hour'])

        # Prepare the input for prediction
        input_data = np.array([[temperature, humidity, windspeed, general_diffuse_flows, hour]])
        input_scaled = scaler.transform(input_data)

        # Make prediction
        prediction = model.predict(input_scaled)
        return render_template('index.html', prediction_text=f"Dự đoán mức tiêu thụ: {prediction[0]:.2f} kWh")
    except Exception as e:
        return render_template('index.html', prediction_text=f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    app.run(debug=True)
