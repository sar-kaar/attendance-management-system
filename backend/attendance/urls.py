from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('codes', views.AttendanceCodeViewSet, basename='attendance-code')
router.register('eca-activities', views.ECAActivityViewSet, basename='eca-activity')
router.register('', views.AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
