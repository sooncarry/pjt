from django.urls import path
from .views import signup_view, check_username, ActivateAccountView
from .views import MyPageView
from .views import financial_profile_view

urlpatterns = [
    path('signup/', signup_view),
    path('check-username/', check_username, name='check-username'),
    path('mypage/', MyPageView.as_view(), name='mypage'),
    path('financial-profile/', financial_profile_view),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
]
