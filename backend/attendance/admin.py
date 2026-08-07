from django.contrib import admin

from .models import Attendance, AttendanceCode, ECAActivity

admin.site.register(Attendance)
admin.site.register(AttendanceCode)
admin.site.register(ECAActivity)
