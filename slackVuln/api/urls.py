from django.urls import path
from .views import button_clicked

urlpatterns = [
    path('slack/interact/', button_clicked)
]