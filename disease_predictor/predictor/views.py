# predictor/views.py
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .ml_model import predict_breast_cancer,predict_heart_disease,predict_parkinsons_disease
from django.contrib.auth import authenticate, login 
from django.contrib import messages
from predictor.models import User, PatientProfile, Patient,Gp,MedicalSpecialist
from predictor.util import is_user_name_unique


feature_names_breast_cancer = ['mean radius', 'mean texture', 'mean perimeter', 'mean area',
                     'mean smoothness', 'mean compactness', 'mean concavity',
                     'mean concave points', 'mean symmetry', 'mean fractal dimension',
                     'radius error', 'texture error', 'perimeter error', 'area error',
                     'smoothness error', 'compactness error', 'concavity error',
                     'concave points error', 'symmetry error', 'fractal dimension error',
                     'worst radius', 'worst texture', 'worst perimeter', 'worst area',
                     'worst smoothness', 'worst compactness', 'worst concavity',
                     'worst concave points', 'worst symmetry', 'worst fractal dimension']

feature_names_heart_disease = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach',
    'exang', 'oldpeak', 'slope', 'ca', 'thal'
]

feature_names_parkinsons_disease = [
    'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)',
    'MDVP:Jitter(Abs)', 'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP',
    'MDVP:Shimmer', 'MDVP:Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5',
    'MDVP:APQ', 'Shimmer:DDA', 'NHR', 'HNR', 'RPDE', 'DFA',
    'spread1', 'spread2', 'D2', 'PPE'
]


def home_view(request):
    return render(request, 'home.html')

def diagnoser_view(request):
    return render(request, 'diagnoser.html', {'feature_names_breast_cancer': feature_names_breast_cancer ,'feature_names_heart_disease':feature_names_heart_disease,'feature_names_parkinsons_disease':feature_names_parkinsons_disease})

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

           
        canser_data = [13.28, 20.28, 87.32, 545.2, 0.1041, 0.1436, 0.09847, 0.06158, 0.1974, 0.06782, 0.3704, 0.8249, 2.427, 31.33, 0.005072, 0.02147, 0.02185, 0.00956, 0.01719, 0.003317, 17.38, 28, 113.1, 907.2, 0.153, 0.3724, 0.3664, 0.1492, 0.3739, 0.1027]
        non_canser_data =[8.196, 16.84, 51.71, 201.9, 0.086, 0.05943, 0.01588, 0.005917, 0.1769, 0.06503, 0.1563, 0.9567, 1.094, 8.205, 0.008968, 0.01646, 0.01588, 0.005917, 0.02574, 0.002582, 8.964, 21.96, 57.26, 242.2, 0.1297, 0.1357, 0.0688, 0.02564, 0.3105, 0.07409]        
        prediction = predict_breast_cancer(canser_data) 

        return render(request,'breast_cancer_prediction.html',{'prediction': prediction})
        #return HttpResponse("Data captured successfully!\n" + str(captured_data)+result)

    return HttpResponse("Invalid request method. Only POST requests are allowed.")

def heart_disease_prediction(request):
    if request.method == 'POST':
        
        captured_data = []

        for feature in feature_names_heart_disease:
            # Retrieve data from POST request using feature names
            data_value = request.POST.get(feature)

            try:
                data_value_float = float(data_value)
                captured_data.append(data_value_float)
            except (ValueError, TypeError):
                # Handle the case where conversion to float fails
                print(f"Could not convert {feature} value to float: {data_value}")

           
        captured_data = [63,1,3,145,233,1,0,150,0,2.3,0,0,1]
        #captured_data = [67,1,0,120,229,0,0,129,1,2.6,1,2,3]     
        prediction = predict_heart_disease(captured_data) 

        return render(request,'heart_disease_prediction.html',{'prediction': prediction})
        #return HttpResponse("Data captured successfully!\n" + str(captured_data)+result)

    return HttpResponse("Invalid request method. Only POST requests are allowed.")

def parkinsons_prediction(request):
    if request.method == 'POST':
        
        captured_data = []

        for feature in feature_names_heart_disease:
            # Retrieve data from POST request using feature names
            data_value = request.POST.get(feature)

            try:
                data_value_float = float(data_value)
                captured_data.append(data_value_float)
            except (ValueError, TypeError):
                # Handle the case where conversion to float fails
                print(f"Could not convert {feature} value to float: {data_value}")

           
        #captured_data = [197.07600,206.89600,192.05500,0.00289,0.00001,0.00166,0.00168,0.00498,0.01098,0.09700,0.00563,0.00680,0.00802,0.01689,0.00339,26.77500,0.422229,0.741367,-7.348300,0.177551,1.743867,0.085569]
        captured_data = [150.44000, 163.44100, 144.73600, 0.00396, 0.00003, 0.00206, 0.00233, 0.00619, 0.02551, 0.23700, 0.01321, 0.01574, 0.02148, 0.03964, 0.00611, 23.13300, 0.352396, 0.759320, -6.261446, 0.183218, 2.264226, 0.144105]     
        prediction = predict_parkinsons_disease(captured_data) 

        return render(request,'parkinsons_disease_prediction.html',{'prediction': prediction})
        #return HttpResponse("Data captured successfully!\n" + str(captured_data)+result)

    return HttpResponse("Invalid request method. Only POST requests are allowed.")


def breast_cancer_info__view(request):
    return render(request, 'breast_cancer_info.html')

def specialist_consultant__view(request):
    return render(request, 'specialist_consultant.html')

def heart_disease_info_view(request):
    return render(request, 'heart_disease_info.html')

def parkinsons_disease_info_view(request):
    return render(request, 'parkinsons_disease_info.html')

def user_login_form(request):
    return render(request, 'login.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('diagnoser')  # Redirect to home page after login
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login_form')  # Redirect back to login page with error message
    
    messages.error(request, 'Invalid username or password.')
    return render(request, 'login_form') 

def user_reg_form(request):
    return render(request, 'admin_user_reg.html')

def create_patient(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        username = request.POST.get('username')
        password = request.POST.get('password')

        uniqueUserName = is_user_name_unique(username)
        
        if uniqueUserName:
            try:
                # Create a new User object with the role set to "PATIENT"
                patient = Patient.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, role=User.Role.PATIENT)
                # Create a new PatientProfile object associated with the user
                patient_profile = PatientProfile.objects.create(user=patient, gender=gender, dob=dob, address=address)

                if (patient is not None and patient_profile is not None):
                    messages.success(request, 'User Created successfully!')
                    return redirect('user_reg_form')
                else:
                    messages.error(request, 'User Creatating Erorr!')
                    return redirect('user_reg_form')
            except Exception as e:
                return redirect('user_reg_form')
        else:
            messages.error(request, 'this user name is alrady taken Try another one!')
            return redirect('user_reg_form')

    else:
        messages.error(request, 'something went wrong!')
        return redirect('user_reg_form')
        
        

    
def create_gp(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        uniqueUserName = is_user_name_unique(username)
        
        if uniqueUserName:
            try:
                gp = Gp.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, role=User.Role.GP)
                if (gp is not None):
                    messages.success(request, 'User Created successfully!')
                    return redirect('gp_reg_form')
                else:
                    messages.error(request, 'User Creatating Erorr!')
                    return redirect('gp_reg_form')
            except Exception as e:
                return redirect('gp_reg_form')
        else:
            messages.error(request, 'this user name is alrady taken Try another one!')
            return redirect('gp_reg_form')

    else:
        messages.error(request, 'something went wrong!')
        return redirect('gp_reg_form')

def manage_users(request):

    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})







    