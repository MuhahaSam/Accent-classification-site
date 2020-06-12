from django.db import models
from django.contrib.auth.models import User
import os.path
# Create your models here.



class Data(models.Model):
    record = models.FileField(upload_to='audio/')
    date = models.DateTimeField(auto_now=True)
    data_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.record)

    class Meta:
        ordering = ['-date']

class Result(models.Model):
    result = models.FloatField()
    data_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.result)


    class Meta:
        ordering = ['-date']



# Create your models here.
