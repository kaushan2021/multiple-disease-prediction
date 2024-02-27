from django.db.models import TextChoices


class DiseaseType(TextChoices):
    HEART = 'Heart', 'Heart Disease'
    PARKINSON = 'Parkinson', 'Parkinson Disease'
    BREAST = 'Breast', 'Breast Cancer'

class PredictionResult(TextChoices):
    POSITIVE = 'Positive', 'Positive'
    NEGATIVE = 'Negative', 'Negative'