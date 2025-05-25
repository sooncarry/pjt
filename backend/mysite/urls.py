from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from education.views import finance_terms  # 직접 import
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 계정·토큰·기타 앱
    path('api/',              include('accounts.urls')),
    path('api/token/',        TokenObtainPairView.as_view(),  name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(),      name='token_refresh'),
    path('api/boards/',       include('boards.urls')),
    path('api/stock/',        include('stock.urls')),
    path('api/savings/',      include('savings.urls')),
    path('api/finance/',      include('finance.urls')),
    path('api/finance-terms/', finance_terms, name='finance-terms'),

    # education/urls.py 에 3가지(path) 모두 정의되어 있으므로 한 번만 include
    path('api/', include('education.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
