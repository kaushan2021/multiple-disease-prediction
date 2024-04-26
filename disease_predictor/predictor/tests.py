from datetime import datetime
from unittest.mock import patch
from urllib import request
from django.test import RequestFactory, TestCase, Client
from predictor.enums import DiseaseType
from predictor.ml_model import predict_heart_disease
from predictor.models import PatientProfile, User
from django.urls import reverse

from predictor.views import breast_cancer_prediction, heart_disease_prediction, parkinsons_prediction

class UserLoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password', role='ADMIN')

    def test_user_login_success(self):
        response = self.client.post(reverse('login'), {'username': 'test_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(response.url, '/app/admin_home/')  

    def test_user_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'invalid_user', 'password': 'invalid_password'})
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(response.url, '/app/')

class CreatePatientTestCase(TestCase):
    def test_create_patient_success(self):

        post_data = {
            'first_name': 'Pasindu',
            'last_name': 'Kaushan',
            'email': 'pasiksuan98.com',
            'gender': 'Male',
            'dob': '1998-05-12',
            'address': '123 United Kindom, LongonCity',
            'username': 'K_dot',
            'password': 'Test98',
        }

        def mock_is_user_name_unique(username):
            return True
        
        with patch('predictor.util.is_user_name_unique', side_effect=mock_is_user_name_unique):
            response = self.client.post(reverse('create_patient'), post_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_reg_form'))
        self.assertTrue(User.objects.filter(username='K_dot').exists())
        self.assertTrue(PatientProfile.objects.filter(user__username='K_dot').exists())
        
class PredictHeartDiseaseTestCase(TestCase):
    def test_predict_heart_disease(self):

        features_positive = [63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1]
        features_negative = [67, 1, 0, 120, 229, 0, 0, 129, 1, 2.6, 1, 2, 3]

        prediction_positive = predict_heart_disease(features_positive)
        prediction_negative = predict_heart_disease(features_negative)

        self.assertEqual(prediction_positive, 1)  
        self.assertEqual(prediction_negative, 0)  


class HeartDiseasePredictionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.patient_profile = PatientProfile.objects.create(user=self.user, gender='male', dob='1990-01-01')

    def test_heart_disease_prediction_positive(self):
        captured_data = {
            'patient_id': self.user.id,
            'cp': 3,
            'trestbps': 145,
            'chol': 233,
            'fbs': 1,
            'restecg': 0,
            'thalach': 150,
            'exang': 0,
            'oldpeak': 2.3,
            'slope': 0,
            'ca': 0,
            'thal': 1,
        }
        request = self.factory.post(reverse('heart_disease_prediction'), captured_data)
        request.user = self.user

        response = heart_disease_prediction(request)

        self.assertEqual(response.status_code, 200)  



    def test_heart_disease_prediction_negative(self):
        captured_data = {
            'patient_id': self.user.id,
            'cp': 0,
            'trestbps': 120,
            'chol': 229,
            'fbs': 0,
            'restecg': 0,
            'thalach': 129,
            'exang': 1,
            'oldpeak': 2.6,
            'slope': 1,
            'ca': 2,
            'thal': 3,
        }

        request = self.factory.post(reverse('heart_disease_prediction'), captured_data)
        request.user = self.user

        response = heart_disease_prediction(request)

        self.assertEqual(response.status_code, 200)  

class BreastCancerPredictionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

    def test_breast_cancer_prediction_positive(self):
        captured_data = {
            'patient_id': self.user.id,
            'mean_radius': 13.28,
            'mean_texture': 20.28,
            'mean_perimeter': 87.32,
            'mean_area': 545.2,
            'mean_smoothness': 0.1041,
            'mean_compactness': 0.1436,
            'mean_concavity': 0.09847,
            'mean_concave_points': 0.06158,
            'mean_symmetry': 0.1974,
            'mean_fractal_dimension': 0.06782,
            'radius_error': 0.3704,
            'texture_error': 0.8249,
            'perimeter_error': 2.427,
            'area_error': 31.33,
            'smoothness_error': 0.005072,
            'compactness_error': 0.02147,
            'concavity_error': 0.02185,
            'concave_points_error': 0.00956,
            'symmetry_error': 0.01719,
            'fractal_dimension_error': 0.003317,
            'worst_radius': 17.38,
            'worst_texture': 28,
            'worst_perimeter': 113.1,
            'worst_area': 907.2,
            'worst_smoothness': 0.153,
            'worst_compactness': 0.3724,
            'worst_concavity': 0.3664,
            'worst_concave_points': 0.1492,
            'worst_symmetry': 0.3739,
            'worst_fractal_dimension': 0.1027,
        }

        request = self.factory.post(reverse('breast_cancer_prediction'), captured_data)
        request.user = self.user

        response = breast_cancer_prediction(request)

        self.assertEqual(response.status_code, 200)


    def test_breast_cancer_prediction_negative(self):
        captured_data = {
            'patient_id': self.user.id,
            'mean_radius': 13.28,
            'mean_texture': 20.28,
            'mean_perimeter': 87.32,
            'mean_area': 545.2,
            'mean_smoothness': 0.1041,
            'mean_compactness': 0.1436,
            'mean_concavity': 0.09847,
            'mean_concave_points': 0.06158,
            'mean_symmetry': 0.1974,
            'mean_fractal_dimension': 0.06782,
            'radius_error': 0.3704,
            'texture_error': 0.8249,
            'perimeter_error': 2.427,
            'area_error': 31.33,
            'smoothness_error': 0.005072,
            'compactness_error': 0.02147,
            'concavity_error': 0.02185,
            'concave_points_error': 0.00956,
            'symmetry_error': 0.01719,
            'fractal_dimension_error': 0.003317,
            'worst_radius': 17.38,
            'worst_texture': 28,
            'worst_perimeter': 113.1,
            'worst_area': 907.2,
            'worst_smoothness': 0.153,
            'worst_compactness': 0.3724,
            'worst_concavity': 0.3664,
            'worst_concave_points': 0.1492,
            'worst_symmetry': 0.3739,
            'worst_fractal_dimension': 0.1027,
        }

        request = self.factory.post(reverse('breast_cancer_prediction'), captured_data)
        request.user = self.user

        response = breast_cancer_prediction(request)

        self.assertEqual(response.status_code, 200) 

class ParkinsonsPredictionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

    def test_parkinsons_prediction_positive(self):
        captured_data = {
            'patient_id': self.user.id,
            'MDVP:Fo(Hz)': 150.44000,
            'MDVP:Fhi(Hz)': 163.44100,
            'MDVP:Flo(Hz)': 144.73600,
            'MDVP:Jitter(%)': 0.00396,
            'MDVP:Jitter(Abs)': 0.00003,
            'MDVP:RAP': 0.00206,
            'MDVP:PPQ': 0.00233,
            'Jitter:DDP': 0.00619,
            'MDVP:Shimmer': 0.02551,
            'MDVP:Shimmer(dB)': 0.23700,
            'Shimmer:APQ3': 0.01321,
            'Shimmer:APQ5': 0.01574,
            'MDVP:APQ': 0.02148,
            'Shimmer:DDA': 0.03964,
            'NHR': 0.00611,
            'HNR': 23.13300,
            'RPDE': 0.352396,
            'DFA': 0.759320,
            'spread1': -6.261446,
            'spread2': 0.183218,
            'D2': 2.264226,
            'PPE': 0.144105,
        }

        request = self.factory.post(reverse('parkinsons_prediction'), captured_data)
        request.user = self.user

        response = parkinsons_prediction(request)

        self.assertEqual(response.status_code, 200) 


    def test_parkinsons_prediction_negative(self):
        captured_data = {
            'patient_id': self.user.id,
            'MDVP:Fo(Hz)': 197.07600,
            'MDVP:Fhi(Hz)': 206.89600,
            'MDVP:Flo(Hz)': 192.05500,
            'MDVP:Jitter(%)': 0.00289,
            'MDVP:Jitter(Abs)': 0.00001,
            'MDVP:RAP': 0.00166,
            'MDVP:PPQ': 0.00168,
            'Jitter:DDP': 0.00498,
            'MDVP:Shimmer': 0.01098,
            'MDVP:Shimmer(dB)': 0.09700,
            'Shimmer:APQ3': 0.00563,
            'Shimmer:APQ5': 0.00680,
            'MDVP:APQ': 0.00802,
            'Shimmer:DDA': 0.01689,
            'NHR': 0.00339,
            'HNR': 26.77500,
            'RPDE': 0.422229,
            'DFA': 0.741367,
            'spread1': -7.348300,
            'spread2': 0.177551,
            'D2': 1.743867,
            'PPE': 0.085569,
        }

        request = self.factory.post(reverse('parkinsons_prediction'), captured_data)
        request.user = self.user

        response = parkinsons_prediction(request)

        self.assertEqual(response.status_code, 200) 
