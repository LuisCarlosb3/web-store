from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts.viewsets import UserViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = [
    path("api/", include(router.urls)),
    path('admin/', admin.site.urls),
]
