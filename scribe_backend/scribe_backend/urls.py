"""
URL configuration for scribe_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .api_views import LoginAPI, LogoutAPI, QuestionAPI, ChatAPI, UserAnswerAPI, UserCreateAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/questions/', QuestionAPI.as_view(), name='question_api'),
    path('api/chat/', ChatAPI.as_view(), name='chat_api'),
    path('api/user_answers/', UserAnswerAPI.as_view(), name='user_answer_api'),
    path('api/users/', UserCreateAPI.as_view(), name='user_create'),
    path('api/login/', LoginAPI.as_view(), name='login_api'),
    path('api/logout/', LogoutAPI.as_view(), name='logout_api'),
]
