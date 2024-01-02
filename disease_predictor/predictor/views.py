# predictor/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .ml_model import predict_breast_cancer

def home_view(request):
    return render(request, 'home.html')

def breast_cancer_prediction(request):
    context = {}
    if request.method == 'POST':
        # Assuming you have a form with input fields corresponding to the features
        features = [float(request.POST[f'feature_{i}']) for i in range(1, 31)]
        prediction = predict_breast_cancer(features)
        context['prediction'] = 'Malignant' if prediction == 1 else 'Benign'

    return render(request, 'breast_cancer_prediction.html', context)
