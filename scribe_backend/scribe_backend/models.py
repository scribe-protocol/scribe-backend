# models.py
from django.contrib.auth.models import User
from django.db import models

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField()
    response = models.TextField()

