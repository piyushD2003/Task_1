from django.db import models


class Records(models.Model):
    patient_name = models.CharField(max_length=100)
    date = models.DateField()
    medication = models.JSONField()

    def __str__(self):
        return self.patient_name