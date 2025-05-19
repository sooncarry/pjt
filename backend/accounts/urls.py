from django.urls import path
from .views import signup_view, check_username

urlpatterns = [
    path('signup/', signup_view),
    path('check-username/', check_username, name='check-username'),
]
