from django.urls import path
from .views import SignupView, LoginView, UserDetailAPIView, UpdateUserView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserDetailAPIView.as_view(), name='user-detail'),
    path('update-profile/', UpdateUserView.as_view(), name='update-profile'),
]
