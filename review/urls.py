from django.urls import path
from django.urls import include

from rest_framework.routers import DefaultRouter

reviewRouter = DefaultRouter()

urlpatterns = [
    path("", include(reviewRouter.urls)),
]