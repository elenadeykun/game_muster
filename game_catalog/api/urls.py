from django.conf.urls import url
from . import views

urlpatterns = [
    url('^must$', views.must),
    url('^game$', views.game),
    url('^$', views.home),
]
