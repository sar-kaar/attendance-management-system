from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

# The API surface, mounted below at both `/api/` and `/api/v1/`. `/api/` stays for
# the existing web frontend (backward-compatible); `/api/v1/` is the stable,
# explicitly-versioned base URL mobile clients should pin to (see B8 / the mobile
# API contract doc). They resolve to the same views until a v2 diverges.
api_urlpatterns = [
    path('auth/', include('accounts.urls')),
    path('students/', include('students.urls')),
    path('', include('courses.urls')),
    path('attendance/', include('attendance.urls')),
    path('face/', include('face.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('devices/', include('notifications.urls')),
]

urlpatterns = [
    path('', RedirectView.as_view(url=settings.FRONTEND_URL), name='root-redirect'),
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urlpatterns)),
    path('api/', include(api_urlpatterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
