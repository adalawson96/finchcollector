from django.db import models

# Create your models here.
name = models.CharField(max_length=100)
origin = models.CharField(max_length=100)
description = models.TextField(max_length=250)
age = models.IntegerField()

    #changing this instance method does not impact the database, therefore no makemigrations is necessaary

