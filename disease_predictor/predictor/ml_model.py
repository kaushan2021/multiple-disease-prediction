import numpy as np
import pickle
import os
from django.conf import settings
from sklearn.preprocessing import StandardScaler


def predict_breast_cancer(features):

    # Load the trained model
    server_path = os.path.dirname(__file__)
    ml_model_folder = os.path.join(server_path, 'Ml_Models')       
    model_file_path = os.path.join(ml_model_folder,'breast_cancer_prediction_model.sav') 

    model = pickle.load(open(model_file_path, 'rb'))

    
    sample_input = np.array(features).reshape(1, -1)
    scaler = StandardScaler()
    features_data_reshaped = scaler.fit_transform(sample_input)

    # Make prediction 
    prediction = model.predict(features_data_reshaped)

    prediction_result = int(prediction[0])
    
    return prediction_result