from django.conf.urls import url
from websocket.views import user_list, log_in, log_out

from . import views
from . import consumers 

app_name = 'websocket'

urlpatterns = [
    url(r'^log_in/$', views.log_in, name='log_in'),
    url(r'^log_out/$', views.log_out, name='log_out'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^$', views.user_list, name='user_list'),
]