from rest_framework import serializers
from .models import Question, UserAnswer, User


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question"]


class UserAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)  # Nesting the serializer

    class Meta:
        model = UserAnswer
        fields = ["id", "question", "response"]  # 'question' now includes detailed info


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
