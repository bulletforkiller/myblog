from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.auth, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('user_detail/', views.user_detail, name='user_detail'),
    path('change_nickname/', views.change_nickname, name='change_nickname'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('send_code/', views.send_code, name='send_code'),
]
