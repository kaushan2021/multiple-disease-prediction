# predictor/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .ml_model import predict_breast_cancer

feature_names_breast_cancer = ['mean radius', 'mean texture', 'mean perimeter', 'mean area',
                     'mean smoothness', 'mean compactness', 'mean concavity',
                     'mean concave points', 'mean symmetry', 'mean fractal dimension',
                     'radius error', 'texture error', 'perimeter error', 'area error',
                     'smoothness error', 'compactness error', 'concavity error',
                     'concave points error', 'symmetry error', 'fractal dimension error',
                     'worst radius', 'worst texture', 'worst perimeter', 'worst area',
                     'worst smoothness', 'worst compactness', 'worst concavity',
                     'worst concave points', 'worst symmetry', 'worst fractal dimension']

def home_view(request):
    return render(request, 'home.html')

def diagnoser_view(request):

    
    return render(request, 'diagnoser.html', {'feature_names_breast_cancer': feature_names_breast_cancer})

def breast_cancer_prediction(request):
    if request.method == 'POST':
        
        captured_data = []

        for feature in feature_names_breast_cancer:
            # Retrieve data from POST request using feature names
            data_value = request.POST.get(feature)

            try:
                data_value_float = float(data_value)
                captured_data.append(data_value_float)
            except (ValueError, TypeError):
                # Handle the case where conversion to float fails
                print(f"Could not convert {feature} value to float: {data_value}")

           
        feature_inputs = [14.5, 21.2, 98.0, 654.3, 0.102, 0.107, 0.081, 0.066, 0.176, 0.059, 0.271, 0.792, 2.613, 26.5, 0.005, 0.022, 0.020, 0.007, 0.025, 0.004, 15.3, 28.8, 98.0, 708.8, 0.127, 0.345, 0.391, 0.109, 0.198, 0.06]
        prediction = predict_breast_cancer(feature_inputs)
        
        if prediction == 1:
            result = "negative"
        result = "possitive"    

        return HttpResponse("Data captured successfully!\n" + str(captured_data)+result)

    return HttpResponse("Invalid request method. Only POST requests are allowed.")

