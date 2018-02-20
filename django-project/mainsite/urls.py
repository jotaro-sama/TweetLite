from django.urls import path, re_path

from . import views

app_name = 'mainsite'

urlpatterns = [
    path('', views.index, name='index'),
    path('logged/', views.logged, name='logged'),
    #path('sign/', views.sign, name='sign'),
    path('sign/', views.sign, name='sign')
]