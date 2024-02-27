from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        PATIENT = "PATIENT", "Patient"
        GP = "GP", "GP"
        MEDICAL_SPECIALIST = "MEDICAL_SPECIALIST", "Medical Specialist"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


#Patient Model
class PatientManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.PATIENT)


class Patient(User):

    base_role = User.Role.PATIENT

    patient = PatientManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Patient"




class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female"), ("other", "Other")], null=True)
    dob = models.DateField(null=True)
    address = models.CharField(max_length=255, null=True)


#Medical Specialist Model
class MedicalSpecialistManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.MEDICAL_SPECIALIST)


class MedicalSpecialist(User):

    base_role = User.Role.MEDICAL_SPECIALIST

    Medical_Specialist = MedicalSpecialistManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Medical Specialist"


class MedicalSpecialistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialis_area = models.CharField(max_length=50, null=True)


#GP Model
class GpManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.GP)


class Gp(User):

    base_role = User.Role.GP

    teacher = GpManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Gp"


class GpProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disease_type = models.CharField(max_length=100)
    result = models.TextField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report ID: {self.report_id}, User: {self.user.username}, Disease Type: {self.disease_type}"    
    


