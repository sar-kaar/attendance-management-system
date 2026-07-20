from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register('users', views.AdminUserViewSet, basename='admin-user')

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.UserDetailView.as_view(), name='user_detail'),
    path('otp/send/', views.OTPSendView.as_view(), name='otp_send'),
    path('otp/verify/', views.OTPVerifyView.as_view(), name='otp_verify'),
    path('', include(router.urls)),
]
