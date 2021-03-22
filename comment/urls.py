from django.urls import path
from django.urls import include

from rest_framework.routers import DefaultRouter

commentRouter = DefaultRouter()

urlpatterns = [
    path("", include(commentRouter.urls)),
]