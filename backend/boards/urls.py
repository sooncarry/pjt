from django.urls import path
from .views import PostListCreateView, PostRetrieveUpdateDestroyView, CommentCreateView, CommentUpdateDeleteView, toggle_like

urlpatterns = [
    path('', PostListCreateView.as_view()),          # /api/boards/
    path('<int:pk>/', PostRetrieveUpdateDestroyView.as_view()),  # /api/boards/<id>/
    path('<int:pk>/like/', toggle_like),
    path('comments/', CommentCreateView.as_view()),
    path('comments/<int:pk>/', CommentUpdateDeleteView.as_view()),
]
