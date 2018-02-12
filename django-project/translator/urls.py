from django.urls import path, re_path

from . import views

app_name = 'translator'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^text=+(?P<text>.+)/$', views.translate, name='translate'),
]