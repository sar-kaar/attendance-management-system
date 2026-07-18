from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.AttendanceViewSet)
router.register('codes', views.AttendanceCodeViewSet, basename='attendance-code')

urlpatterns = [
    path('', include(router.urls)),
]
