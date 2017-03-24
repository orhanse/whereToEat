from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='app'),
    url(r'^setCR$', views.setCR, name='setcr'),
    url(r'^startApp$', views.startApp, name='startApp'),
    url(r'^reset', views.resetApp, name='reset'),
]
