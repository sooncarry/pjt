from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChallengeTemplateViewSet, SavingChallengeViewSet

router = DefaultRouter()
router.register(r'templates', ChallengeTemplateViewSet)
router.register(r'challenges', SavingChallengeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
