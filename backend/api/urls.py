from django.urls import path
from .views import imageModel

urlpatterns = [
    path("image-model",imageModel),
]
