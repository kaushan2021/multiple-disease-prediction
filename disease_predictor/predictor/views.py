# predictor/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .ml_model import predict_breast_cancer

def home_view(request):
    return render(request, 'home.html')

def diagnoser_view(request):
    feature_names_breast_cancer = ['mean radius', 'mean texture', 'mean perimeter', 'mean area',
                     'mean smoothness', 'mean compactness', 'mean concavity',
                     'mean concave points', 'mean symmetry', 'mean fractal dimension',
                     'radius error', 'texture error', 'perimeter error', 'area error',
                     'smoothness error', 'compactness error', 'concavity error',
                     'concave points error', 'symmetry error', 'fractal dimension error',
                     'worst radius', 'worst texture', 'worst perimeter', 'worst area',
                     'worst smoothness', 'worst compactness', 'worst concavity',
                     'worst concave points', 'worst symmetry', 'worst fractal dimension']
    
    return render(request, 'diagnoser.html', {'feature_names_breast_cancer': feature_names_breast_cancer})

def breast_cancer_prediction(request):
    context = {}
    if request.method == 'POST':
        # Assuming you have a form with input fields corresponding to the features
        features = [float(request.POST[f'feature_{i}']) for i in range(1, 31)]
        prediction = predict_breast_cancer(features)
        context['prediction'] = 'Malignant' if prediction == 1 else 'Benign'

    return render(request, 'breast_cancer_prediction.html', context)

