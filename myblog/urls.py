from django.urls import path
from . import views

app_name = 'myblog'
urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_id>', views.blog_detail, name='blog_detail'),
    path(
        'type/<int:blogs_with_type>',
        views.blogs_with_type,
        name='blog_with_type'),
    path(
        'date/<int:year>/<int:month>',
        views.blogs_by_date,
        name='blogs_by_date'),
]
