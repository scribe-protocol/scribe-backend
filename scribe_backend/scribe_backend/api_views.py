from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Question, UserAnswer
from .serializers import QuestionSerializer, UserAnswerSerializer
from openai import OpenAI
import os
from dotenv import load_dotenv
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

load_dotenv()

# Access environment variables
api_key = os.environ.get("OPENAI_API_KEY")
project_id = os.environ.get("OPENAI_PROJECT_ID")
org_id = os.environ.get("OPENAI_ORG_ID")


class UserAnswerAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions = UserAnswer.objects.filter(user=request.user)
        serializer = UserAnswerSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        for question_id, response in request.data.items():
            if question_id.startswith("question_"):
                question_id = question_id.split("_")[1]
                UserAnswer.objects.update_or_create(
                    user=request.user,
                    question_id=question_id,
                    defaults={"response": response},
                )
        return Response({"status": "success"})


class ChatAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_input = request.data.get("user_input")

        # Format the context with questions and answers for readability
        user_answers = UserAnswer.objects.filter(user=request.user).select_related(
            "question"
        )
        context_list = [
            f"Q: {answer.question.question} A: {answer.response}"
            for answer in user_answers
        ]
        context_str = "\n".join(context_list)

        # Define the system message with instructions for the assistant
        system_message = (
            "You are a helpful assistant trained on a mix of general knowledge and user-specific knowledge. "
            "You have access to the user's answers to various questions, which are structured in the format:\n\n"
            "Q: [Question text] A: [User's answer]\n\n"
            "Use these answers to inform your responses where relevant, adapting them to address the user's input."
        )

        # Initialize OpenAI client
        client = OpenAI(api_key=api_key, project=project_id, organization=org_id)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"{system_message}\n\n{context_str}"},
                {"role": "user", "content": user_input},
            ],
            temperature=1,
            max_tokens=4095,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        return Response(response.choices[0].message.content)


class QuestionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class UserCreateAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        try:
            user = User.objects.create_user(
                username=data.get("email"),
                email=data.get("email"),
                password=data.get("password"),
            )
            user.first_name = data.get("first_name", "")
            user.last_name = data.get("last_name", "")
            user.save()
            return Response(
                {"message": "User created successfully"}, status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    permission_classes = [
        AllowAny
    ]  # Allow any user (authenticated or not) to access this view

    def post(self, request):
        # You can allow users to login with either username or email
        username = request.data.get("username") or request.data.get("email")
        password = request.data.get("password")

        if username is None or password is None:
            return Response(
                {"error": "Please provide both username/email and password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Get or create a token for the user
        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=status.HTTP_200_OK)


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Delete the user's token to log them out
            request.user.auth_token.delete()
            return Response(
                {"message": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        except:
            return Response(
                {"error": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST
            )
