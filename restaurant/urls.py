from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'Rest', views.getRestaurant, name='getRest'),
     url(r'status', views.setStatus, name='getRest'),
     url(r'update', views.update, name='upRest'),
     url(r'delete', views.delete, name='delRest'),
]
