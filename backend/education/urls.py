from django.urls import path
from .views import finance_terms, breaking_news, quiz_question_list


urlpatterns = [
    path('finance-terms/', finance_terms, name='finance-terms'),
    path('breaking-news/', breaking_news, name='breaking-news'),
    path('quiz/', quiz_question_list, name='quiz-list'),
]
