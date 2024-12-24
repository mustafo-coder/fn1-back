from django.urls import path, include
from .views import (
    ArticleListAPIView,
    ArticleCreateAPIView,
    ArticleUpdateAPIView,
    ArticleDeleteAPIView,
    ArticleRetrieveAPIView,
    ArticleSearchAPIView
)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('articles/', ArticleListAPIView.as_view(), name='article-list'),
    path('articles/create/', ArticleCreateAPIView.as_view(), name='article-create'),
    path('articles/<int:pk>/update/', ArticleUpdateAPIView.as_view(), name='article-update'),
    path('articles/<int:pk>/delete/', ArticleDeleteAPIView.as_view(), name='article-delete'),
    path('article/<int:pk>/', ArticleRetrieveAPIView.as_view(), name='article-retrieve'),
    path('articles/search/', ArticleSearchAPIView.as_view(), name='article-search'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)