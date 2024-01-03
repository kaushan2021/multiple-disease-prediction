import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler


def predict_breast_cancer(features):
    # Load the trained model
    #model = joblib.load('./breast_cancer_prediction_model.pkl')
    # Specify the path to your pickle file
    model_file_path = "/Users/pasindukaushan/Desktop/fyp/Project_CodeBase/multiple-disease-prediction/disease_predictor/predictor/Ml_Models/breast_cancer_prediction_model.sav"

    model = pickle.load(open(model_file_path, 'rb'))

    #sample_input = np.array(features).reshape(1, -1)

    # Scale the sample input using the same scaler used for training
    sample_input = np.array([14.5, 21.2, 98.0, 654.3, 0.102, 0.107, 0.081, 0.066, 0.176, 0.059, 0.271, 0.792, 2.613, 26.5, 0.005, 0.022, 0.020, 0.007, 0.025, 0.004, 15.3, 28.8, 98.0, 708.8, 0.127, 0.345, 0.391, 0.109, 0.198, 0.06]).reshape(1, -1)
    scaler = StandardScaler()
    features_data_reshaped = scaler.fit_transform(sample_input)

    # Make prediction 
    prediction = model.predict(features_data_reshaped)

    prediction_result = int(prediction[0])
    
    return prediction_result