from django.urls import path, include

from rest_framework import routers
from api import views

router = routers.DefaultRouter()

# router.register(r'user', views.UserViewSet,'user')
# router.register(r'doctor', views.DoctorViewSet,'doctor')
router.register(r'imageprocess', views.imageprocess,'imageprocess' )
urlpatterns = [
    path('',include(router.urls))
]

