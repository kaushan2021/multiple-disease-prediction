import numpy as np
import pickle
import os
from django.conf import settings

def predict_breast_cancer(features):

    server_path = os.path.dirname(__file__)
    ml_model_folder = os.path.join(server_path, 'Ml_Models')       
    model_file_path = os.path.join(ml_model_folder,'breast_cancer_prediction_model.sav') 

    model = pickle.load(open(model_file_path, 'rb'))
    input_data_as_numpy_array = np.asarray(features)
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
    prediction = model.predict(input_data_reshaped)
    prediction_result = int(prediction[0])
    
    return prediction_result

def predict_heart_disease(features):

    server_path = os.path.dirname(__file__)
    ml_model_folder = os.path.join(server_path, 'Ml_Models')       
    model_file_path = os.path.join(ml_model_folder,'heart_disease_prediction_model.sav') 

    model = pickle.load(open(model_file_path, 'rb'))
    input_data_as_numpy_array = np.asarray(features)
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
    prediction = model.predict(input_data_reshaped)
    prediction_result = int(prediction[0])
    
    return prediction_result

def predict_parkinsons_disease(features):

    server_path = os.path.dirname(__file__)
    ml_model_folder = os.path.join(server_path, 'Ml_Models')       
    model_file_path = os.path.join(ml_model_folder,'parkinsons_disease_prediction_model.sav') 

    model = pickle.load(open(model_file_path, 'rb'))
    input_data_as_numpy_array = np.asarray(features)
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
    prediction = model.predict(input_data_reshaped)
    prediction_result = int(prediction[0])
    
    return prediction_result