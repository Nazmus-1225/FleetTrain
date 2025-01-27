import requests
import joblib
import pandas as pd

# Fetch the model from the Flask API
url = 'http://192.168.0.100:5000/get-model'
response = requests.get(url)

if response.status_code == 200:
    # Save the model file locally
    with open('downloaded_model.pkl', 'wb') as f:
        f.write(response.content)

    # Load the model
    clf = joblib.load('downloaded_model.pkl')

    # Example new data to infer on (ensure it has the same features as your training data)
    dummy_row = pd.DataFrame({
    'age': [50],            # Example: 50 years old
    'sex': [1],             # Example: Male (assuming 1 is for male)
    'cp': [0],              # Example: Type 0 chest pain
    'trestbps': [130],      # Example: Resting blood pressure 130
    'chol': [250],          # Example: Cholesterol 250
    'fbs': [0],             # Example: Fasting blood sugar less than 120 mg/dl
    'restecg': [0],         # Example: Normal resting electrocardiographic result
    'thalach': [150],       # Example: Maximum heart rate achieved
    'exang': [0],           # Example: No exercise induced angina
    'oldpeak': [1.2],       # Example: Depression induced by exercise
    'slope': [1],           # Example: Slope of the peak exercise ST segment
    'ca': [0],              # Example: No major vessels colored by fluoroscopy
    'thal': [2]             # Example: Thalassemia (2: fixed defect)
})

    # Make predictions
    predictions = clf.predict(dummy_row)

    # Output the predictions
    print("Predictions:", predictions)
else:
    print("Failed to retrieve model:", response.status_code)
