# models.py
from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    question = models.CharField()


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.TextField()
