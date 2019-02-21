from django.urls import path
from . import views

urlpatterns = [
    path('like_change', views.like_state_change, name='likechange'),
]
