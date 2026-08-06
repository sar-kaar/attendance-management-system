from django.urls import path

from . import views

urlpatterns = [
    path('', views.DeviceListView.as_view(), name='device_list'),
    path('register/', views.DeviceRegisterView.as_view(), name='device_register'),
    path('unregister/', views.DeviceUnregisterView.as_view(), name='device_unregister'),
]
