from django.db import models

# Create your models here.
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name
