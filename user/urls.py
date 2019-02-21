from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.auth, name='login'),
    path('register/', views.register, name='register'),
    path('logout', views.logout_user, name='logout'),
    path('user_detail', views.user_detail, name='user_detail'),
]
