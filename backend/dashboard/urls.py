from django.urls import path
from . import views

urlpatterns = [
    path('programs/', views.program_list, name='dashboard-programs'),
    path('sections/', views.section_list, name='dashboard-sections'),
    path('students/', views.student_search, name='dashboard-students'),
    path('students/<int:student_id>/attendance/', views.student_attendance_breakdown, name='dashboard-student-attendance'),
    path('attendance-stats/', views.attendance_stats, name='dashboard-attendance-stats'),
    path('at-risk/', views.at_risk_students, name='dashboard-at-risk'),
    path('faculty-performance/', views.faculty_performance, name='dashboard-faculty-performance'),
    path('chronic-latecomers/', views.chronic_latecomers, name='dashboard-chronic-latecomers'),
    path('incomplete-records/', views.incomplete_records, name='dashboard-incomplete-records'),
    path('master-data/import/', views.master_data_import, name='dashboard-master-data-import'),
]
