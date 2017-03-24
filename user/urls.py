from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'showUsers/', views.showUsers, name='showUsers'),
    url(r'getUser', views.getUser, name='getUser'),
    url(r'addUser/', views.addUser, name='add'),
    url(r'updateDirect', views.updateDirect, name='updateDirect'),
    url(r'update', views.update, name='update'),
    url(r'delete', views.delete, name='delete'),
]
