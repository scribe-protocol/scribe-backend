from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserAnswer
from .serializers import UserAnswerSerializer
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Access environment variables
api_key = os.environ.get('OPENAI_API_KEY')
project_id = os.environ.get('OPENAI_PROJECT_ID')
org_id = os.environ.get('OPENAI_ORG_ID')

class QuestionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions = UserAnswer.objects.filter(user=request.user)
        serializer = UserAnswerSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        for question_id, answer in request.data.items():
            if question_id.startswith('question_'):
                question_id = question_id.split('_')[1]
                UserAnswer.objects.update_or_create(
                    user=request.user,
                    question_id=question_id,
                    defaults={'answer': answer}
                )
        return Response({"status": "success"})

class ChatAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_input = request.data.get('user_input')
        context = UserAnswer.objects.filter(user=request.user).values_list('answer', flat=True)
        context_str = " ".join(context)

        client = OpenAI(api_key=api_key, project=project_id, organization=org_id)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": context_str},
                {"role": "user", "content": user_input}
            ],
            temperature=1,
            max_tokens=4095,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return Response({'response': response.choices[0].message['content']})
