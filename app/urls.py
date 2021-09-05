from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('app/', include('fraud_detection.urls')),
    path('admin/', admin.site.urls),
]
