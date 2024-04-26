# predictor/views.py
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse
from .ml_model import predict_breast_cancer,predict_heart_disease,predict_parkinsons_disease
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from predictor.models import User, PatientProfile, Patient,Gp,MedicalSpecialist,MedicalSpecialistProfile,Report,Appointment
from predictor.util import calculate_age, email_alert, generate_medical_report, is_user_name_unique ,feature_names_breast_cancer,feature_names_heart_disease,feature_names_parkinsons_disease
from django.core.serializers import serialize
from .enums import DiseaseType,PredictionResult
from datetime import date, datetime

def gp_home_view(request):
    return render(request, 'home.html')

def diagnoser_view(request):
    userId = request.GET.get('userId')
    if userId != None:
        patient = get_object_or_404(User, id=userId)
        patientId = patient.pk
    return render(request, 'diagnoser.html', {'feature_names_breast_cancer': feature_names_breast_cancer ,'feature_names_heart_disease':feature_names_heart_disease,'feature_names_parkinsons_disease':feature_names_parkinsons_disease,'patient_id':userId})

def breast_cancer_prediction(request):
    if request.method == 'POST':
        
        captured_data = []

        for feature in feature_names_breast_cancer:
            data_value = request.POST.get(feature)

            try:
                data_value_float = float(data_value)
                captured_data.append(data_value_float)
            except (ValueError, TypeError):
                print(f"Could not convert {feature} value to float: {data_value}")

           
        canser_data = [13.28, 20.28, 87.32, 545.2, 0.1041, 0.1436, 0.09847, 0.06158, 0.1974, 0.06782, 0.3704, 0.8249, 2.427, 31.33, 0.005072, 0.02147, 0.02185, 0.00956, 0.01719, 0.003317, 17.38, 28, 113.1, 907.2, 0.153, 0.3724, 0.3664, 0.1492, 0.3739, 0.1027]
        non_canser_data =[8.196, 16.84, 51.71, 201.9, 0.086, 0.05943, 0.01588, 0.005917, 0.1769, 0.06503, 0.1563, 0.9567, 1.094, 8.205, 0.008968, 0.01646, 0.01588, 0.005917, 0.02574, 0.002582, 8.964, 21.96, 57.26, 242.2, 0.1297, 0.1357, 0.0688, 0.02564, 0.3105, 0.07409]        
        prediction = predict_breast_cancer(canser_data) 

        if prediction == 0:
            prediction_result = PredictionResult.POSITIVE
        else:
            prediction_result = PredictionResult.NEGATIVE

        try:
            userId = request.POST.get('patient_id')
            if userId != None:
                patient = get_object_or_404(User, id=userId)
            report = Report.objects.create(user=patient,disease_type=DiseaseType.BREAST,result=prediction_result,created_date=datetime.now())
            report.save()

            #sending medical report email alert
            subject = "Your Test Result"
            to = patient.email
            patient_name = patient.first_name +" "+patient.last_name
            disease_type =DiseaseType.BREAST
            result = prediction_result
            body = generate_medical_report(patient_name, disease_type, result)

            email_alert(subject, body, to)

        except (ValueError, TypeError): 
               print(f"Could not convert {feature} value to float: {data_value}")

        return render(request,'breast_cancer_prediction.html',{'prediction': prediction})

    return HttpResponse("Invalid request method. Only POST requests are allowed.")

def heart_disease_prediction(request):
    if request.method == 'POST':

        captured_data = []

        patient_id = request.POST.get('patient_id')
        patientProfile = get_object_or_404(PatientProfile, user_id=patient_id)
        
        #getting dob of patient from db
        patient_dob = patientProfile.dob
        patient_age = calculate_age(patient_dob)
        #add parient age to the array 
        captured_data.append(patient_age)

        patient_gender = patientProfile.gender
        if patient_gender == "male":
            gender = 1
        if patient_gender == "female":
            gender = 0    
        captured_data.append(gender)

        for feature in feature_names_heart_disease:
            data_value = request.POST.get(feature)

            try:
                data_value_float = float(data_value)
                captured_data.append(data_value_float)
            except (ValueError, TypeError):
                print(f"Could not convert {feature} value to float: {data_value}")
        
        captured_data = [63,1,3,145,233,1,0,150,0,2.3,0,0,1]
        #captured_data = [67,1,0,120,229,0,0,129,1,2.6,1,2,3]     
        prediction = predict_heart_disease(captured_data)

        if prediction ==1:
            prediction_result = PredictionResult.POSITIVE
        else:
            prediction_result = PredictionResult.NEGATIVE

        try:
            #saving resut to database
            user_id = request.POST.get('patient_id')
            patient = get_object_or_404(User, id=user_id)
            report = Report.objects.create(user=patient,disease_type=DiseaseType.HEART,result=prediction_result,created_date=datetime.now())
            report.save()

            #sending medical report email alert
            subject = "Your Test Result"
            to = patient.email
            patient_name = patient.first_name +" "+patient.last_name
            disease_type =DiseaseType.PARKINSON
            result = prediction_result
            body = generate_medical_report(patient_name, disease_type, result)

            email_alert(subject, body, to)

        except (ValueError, TypeError): 
               print(f"Something went wrong{ValueError} {TypeError}")

        return render(request,'heart_disease_prediction.html',{'prediction': prediction})

    return HttpResponse("Invalid request method. Only POST requests are allowed.")

def parkinsons_prediction(request):
    if request.method == 'POST':
        
        captured_data = []

        for feature in feature_names_heart_disease:
            data_value = request.POST.get(feature)

            try:
                data_value_float = float(data_value)
                captured_data.append(data_value_float)
            except (ValueError, TypeError):
                print(f"Could not convert {feature} value to float: {data_value}")

           
        #captured_data = [197.07600,206.89600,192.05500,0.00289,0.00001,0.00166,0.00168,0.00498,0.01098,0.09700,0.00563,0.00680,0.00802,0.01689,0.00339,26.77500,0.422229,0.741367,-7.348300,0.177551,1.743867,0.085569]
        captured_data = [150.44000, 163.44100, 144.73600, 0.00396, 0.00003, 0.00206, 0.00233, 0.00619, 0.02551, 0.23700, 0.01321, 0.01574, 0.02148, 0.03964, 0.00611, 23.13300, 0.352396, 0.759320, -6.261446, 0.183218, 2.264226, 0.144105]     
        prediction = predict_parkinsons_disease(captured_data) 

        if prediction == 1:
            prediction_result = PredictionResult.POSITIVE
        else:
            prediction_result = PredictionResult.NEGATIVE

        try:
            userId = request.POST.get('patient_id')
            if userId != None:
                patient = get_object_or_404(User, id=userId)
            report = Report.objects.create(user=patient,disease_type=DiseaseType.PARKINSON,result=prediction_result,created_date=datetime.now())
            report.save()

            #sending medical report email alert
            subject = "Your Test Result"
            to = patient.email
            patient_name = patient.first_name +" "+patient.last_name
            disease_type =DiseaseType.HEART
            result = prediction_result
            body = generate_medical_report(patient_name, disease_type, result)

            email_alert(subject, body, to)

        except (ValueError, TypeError): 
               print(f"Error : {ValueError} {TypeError}")

        return render(request,'parkinsons_disease_prediction.html',{'prediction': prediction})

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
            if user.role == 'ADMIN':
                return redirect('admin_home_view')
            elif user.role == 'GP':
                return redirect('gp_home')
            elif user.role == 'PATIENT':
                return redirect('patient_home')
            elif user.role == 'MEDICAL_SPECIALIST':
                return redirect('specialist_home')
            else:
                messages.error(request, 'Invalid User.')
                return redirect('login_form')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login_form') 
    
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
                patient = Patient.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, role=User.Role.PATIENT)
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

def create_medical_specialist(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        specialist_area = request.POST.get('specialist_area')
        username = request.POST.get('username')
        password = request.POST.get('password')

        uniqueUserName = is_user_name_unique(username)
        
        if uniqueUserName:
            try:
                medical_specialist = MedicalSpecialist.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, role=User.Role.MEDICAL_SPECIALIST)
                medical_specialist_profile = MedicalSpecialistProfile.objects.create(user=medical_specialist, specialis_area=specialist_area)
                if (medical_specialist is not None and medical_specialist_profile is not None):
                    messages.success(request, 'User Created successfully!')
                    return redirect('medical_specialist_reg_form')
                else:
                    messages.error(request, 'User Creatating Erorr!')
                    return redirect('medical_specialist_reg_form')
            except Exception as e:
                return redirect('medical_specialist_reg_form')
        else:
            messages.error(request, 'this user name is alrady taken Try another one!')
            return redirect('medical_specialist_reg_form')

    else:
        messages.error(request, 'something went wrong!')
        return redirect('medical_specialist_reg_form')

def manage_users(request):

    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

def delete_user(request,user_id):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user_id)
            user.delete()
        except User.DoesNotExist:
            messages.error(request, 'User not found!')
        return redirect('manage_users')
    return redirect('manage_users')

def admin_home_view(request):
    return render(request, 'admin_home.html')

def gp_patient_select(request):
    patients = User.objects.filter(role='PATIENT')
    patients_json = serialize('json', patients, fields=('username', 'first_name', 'last_name'))
    return render(request, 'gp_patient_select.html', {'patients_json': patients_json})

def log_out(request):
    logout(request)
    return redirect('login_form')

def patient_home(request):
    return render(request, 'patient_home.html')

def patient_notification(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        patient_reports = Report.objects.filter(user_id=user_id).order_by('-created_date')
    return render(request, 'patient_notification.html',{'patient_reports': patient_reports})

def patient_appointment_scheduler(request):
    if request.user.is_authenticated:
        user_id = request.user.id
    return render(request, 'appointment_scheduler.html',{'patient_id': user_id})

def desease_education(request):
    return render(request, 'desease_education.html')

def patient_report_result(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            reportId = request.POST.get('report_id')
            patient_reports = Report.objects.filter(report_id=reportId)
            patient_report = patient_reports.first()
            return render(request, 'patient_report.html',{'report': patient_report})
    else:
        messages.error(request, 'please login!')
        return redirect('login_form')

def appointment_scheduler(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            userId = request.user.id
            specialist_type = request.POST.get('specialist_type')
            contact_number = request.POST.get('contact_number')
            appointment_date_str = request.POST.get('appointment_date')
            # Parse the string into a datetime object
            date_object = datetime.fromisoformat(appointment_date_str.replace('Z', '+00:00'))

            # Format the datetime object as needed
            appointment_date = date_object.strftime('%Y-%m-%d %H:%M:%S')
        
            try:    
                user = get_object_or_404(User, id=userId)
                patientProfile = get_object_or_404(PatientProfile,user_id=userId)
                patient_name = patientProfile.user.first_name +" "+patientProfile.user.last_name
                report = Appointment.objects.create(user=user,patient_name = patient_name, specialist_type = specialist_type,contact_number=contact_number, appointment_date =appointment_date,created_date=datetime.now())
                report.save()
                messages.success(request, 'Your appointment is scheduled!')
                return redirect('patient_appointment_scheduler')
               
            except (ValueError, TypeError): 
                print(f"Error value {ValueError} Error type: {TypeError}")
                messages.error(request, 'Something Went Wrong!')
                return redirect('patient_appointment_scheduler')        
    else:
        messages.error(request, 'please login!')
        return redirect('login_form')

def specialist_home(request):
    return render(request, 'specialist_home.html')

def specialist_appoinments(request):
    if request.user.is_authenticated:
        appoinments = Appointment.objects.all()
        return render(request, 'view_appoinments_specialist.html',{'appoinments': appoinments})
    else:
        messages.error(request, 'please login!')
        return redirect('login_form')

def specialist_report_view(request):
    return render(request, 'specialist_patient_report.html')

def medical_history(request):
    return render(request, 'medical_history.html')
