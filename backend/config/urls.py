from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url=settings.FRONTEND_URL), name='root-redirect'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/students/', include('students.urls')),
    path('api/', include('courses.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/face/', include('face.urls')),
    path('api/dashboard/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
