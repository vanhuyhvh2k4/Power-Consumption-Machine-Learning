import tkinter as tk
from tkinter import messagebox
import joblib
import numpy as np

# Load the model and scaler
model = joblib.load("Model/random_forest_model.pkl")
scaler = joblib.load("Model/scaler.pkl")

def predict():
    try:
        # Get input values
        temperature = float(entry_temperature.get())
        humidity = float(entry_humidity.get())
        windspeed = float(entry_windspeed.get())
        general_diffuse_flows = float(entry_general_diffuse_flows.get())
        hour = int(entry_hour.get())

        # Prepare the input for prediction
        input_data = np.array([[temperature, humidity, windspeed, general_diffuse_flows, hour]])
        input_scaled = scaler.transform(input_data)

        # Make prediction
        prediction = model.predict(input_scaled)
        result_label.config(text=f"Dự đoán mức tiêu thụ: {prediction[0]:.2f}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

# Create the GUI window
root = tk.Tk()
root.title("Dự đoán mức tiêu thụ điện năng")

# Input fields
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Nhiệt độ (°C):").grid(row=0, column=0, padx=5, pady=5)
entry_temperature = tk.Entry(frame)
entry_temperature.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Độ ẩm (%):").grid(row=1, column=0, padx=5, pady=5)
entry_humidity = tk.Entry(frame)
entry_humidity.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Tốc độ gió (m/s):").grid(row=2, column=0, padx=5, pady=5)
entry_windspeed = tk.Entry(frame)
entry_windspeed.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Dòng khuếch tán chung:").grid(row=3, column=0, padx=5, pady=5)
entry_general_diffuse_flows = tk.Entry(frame)
entry_general_diffuse_flows.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame, text="Giờ trong ngày (0-23):").grid(row=4, column=0, padx=5, pady=5)
entry_hour = tk.Entry(frame)
entry_hour.grid(row=4, column=1, padx=5, pady=5)

# Predict button
predict_button = tk.Button(root, text="Dự đoán", command=predict)
predict_button.pack(pady=10)

# Result label
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Run the GUI
root.mainloop()
