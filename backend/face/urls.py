from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_face, name='face-register'),
    path('recognize/', views.recognize_face, name='face-recognize'),
    path('mark-attendance/', views.mark_attendance_by_face, name='face-mark-attendance'),
    path('registered/', views.registered_faces, name='face-registered'),
]
