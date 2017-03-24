from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.grading, name='grading'),
    url(r'direct', views.direct, name='direct'),
    url(r'getPoint', views.getPoint, name='getPoint'),
    url(r'reset', views.resetGrading, name='reset'),

]
