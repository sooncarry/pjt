from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChallengeTemplateViewSet,
    current_challenge,
    start_challenge,
    update_current_challenge,
    toggle_check,
    end_challenge,
    active_challenges,
    completed_challenges
)

router = DefaultRouter()
router.register(r'templates', ChallengeTemplateViewSet, basename='template')

urlpatterns = [
    path('', include(router.urls)),

    # 챌린지 API
    path('current/', current_challenge, name='current-challenge'),
    path('start/', start_challenge, name='start-challenge'),
    path('current/update/', update_current_challenge, name='update-challenge'),
    path('check/', toggle_check, name='toggle-check'),
    path('end/', end_challenge, name='end-challenge'),
    path('active/', active_challenges, name='active-challenges'),
    path('history/', completed_challenges, name='completed-challenges'),
]
