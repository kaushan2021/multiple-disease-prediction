import joblib

def predict_breast_cancer(features):
    # Load the trained model
    model = joblib.load('/Users/pasindukaushan/Desktop/fyp/Project_CodeBase/multiple-disease-prediction/disease_predictor/predictor/Ml_Models/breast_cancer_prediction_model.pkl')

    # Make a prediction
    prediction = model.predict([features])
    return prediction[0]