# management/commands/populate_questions.py

from django.core.management.base import BaseCommand
from scribe_backend.models import Question
from django.db import transaction


class Command(BaseCommand):
    help = "Populate the database with predefined questions."

    def handle(self, *args, **kwargs):
        questions = [
            "What is your full name?",
            "When is your birthday?",
            "Where were you born?",
            "What is your current city of residence?",
            "What is your nationality?",
            "What languages do you speak fluently?",
            "What is your preferred name or nickname?",
            "What is your gender identity?",
            "What is your marital status?",
            "Do you have any children? If so, how many and what are their ages?",
            "Do you have any siblings? If so, how many?",
            "Are you close with your extended family?",
            "Do you have any pets? If yes, what kind?",
            "How would you describe your relationship with your parents?",
            "What role does family play in your life?",
            "What is your highest level of education?",
            "What did you study in school/college?",
            "Which school or university did you attend?",
            "Are you currently pursuing any further education or certifications?",
            "What was your favorite subject in school and why?",
            "What is your current occupation?",
            "How long have you been working in your current field?",
            "What do you enjoy most about your job?",
            "What are your career goals for the next five years?",
            "Have you ever changed careers? If so, why?",
            "What are your favorite hobbies or pastimes?",
            "Do you enjoy reading? If so, what genres?",
            "What is your favorite movie or TV show?",
            "Do you play any musical instruments?",
            "What kind of music do you listen to regularly?",
            "Do you follow a specific fitness routine?",
            "How do you maintain your mental well-being?",
            "Do you have any dietary preferences or restrictions?",
            "How important is health and fitness to you?",
            "Do you practice any mindfulness or relaxation techniques?",
            "Are you an early bird or a night owl?",
            "How do you typically spend your weekends?",
            "Do you prefer living in the city, suburbs, or countryside?",
            "How do you balance work and personal life?",
            "What is your favorite way to relax after a long day?",
            "What was your most memorable trip?",
            "Is there a place you have always wanted to visit?",
            "Do you prefer traveling alone or with others?",
            "What is your favorite mode of transportation when traveling?",
            "What is the most adventurous thing you have done?",
            "What type of smartphone do you use?",
            "How much time do you spend on social media daily?",
            "What are your favorite websites or apps?",
            "Do you enjoy gaming? If so, what games do you like?",
            "How do you stay updated with current events?",
            "Do you follow a budget?",
            "What are your financial goals for the next five years?",
            "How do you approach saving and investing?",
            "Do you have any side hustles or additional sources of income?",
            "What is your attitude towards debt?",
            "What values are most important to you?",
            "Do you follow any religious or spiritual beliefs?",
            "What causes or issues are you passionate about?",
            "How do you define success?",
            "What motivates you in life?",
            "How do you typically meet new people?",
            "What qualities do you value in a friend?",
            "How do you handle conflicts in relationships?",
            "Do you enjoy attending social events?",
            "How important is community involvement to you?",
            "Do you engage in any creative activities?",
            "What inspires your creativity?",
            "Have you ever created something you’re proud of?",
            "How do you approach problem-solving?",
            "Do you enjoy brainstorming new ideas?",
            "Where do you see yourself in five years?",
            "What are your long-term life goals?",
            "Do you plan to start any new projects or ventures?",
            "What legacy do you want to leave behind?",
            "How do you envision your ideal life?",
            "What is your proudest personal accomplishment?",
            "Have you overcome any significant challenges in your life?",
            "What are you most grateful for?",
            "What are some of your personal goals?",
            "How do you celebrate your successes?",
            "What subjects did you enjoy most in school?",
            "Do you engage in any lifelong learning activities?",
            "What skills would you like to develop?",
            "Have you taken any online courses or certifications?",
            "What is your preferred learning style?",
            "What professional skills are you currently developing?",
            "Do you mentor or are you being mentored?",
            "What is your proudest career achievement?",
            "How do you handle workplace stress?",
            "What do you think about career growth opportunities in your field?",
            "What is a fun fact about you?",
            "If you could have any superpower, what would it be?",
            "What is your favorite quote or saying?",
            "Who has been the most influential person in your life?",
            "What is something you would like to change about the world?",
            "What is your favorite way to give back to the community?",
            "How do you handle failure?",
            "What is your favorite memory?",
            "Do you have any phobias or fears?",
            "What are you currently passionate about?",
        ]

        created_count = 0
        with transaction.atomic():
            for question in questions:
                obj, created = Question.objects.get_or_create(question=question)
                if created:
                    created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added {created_count} questions to the database."
            )
        )
