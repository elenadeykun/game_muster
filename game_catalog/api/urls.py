from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [

    path('games/', views.GameList.as_view()),
    path(r'games/<int:pk>/', views.GameDetail.as_view()),
    path('musts/', views.MustList.as_view()),
    path(r'genres/', views.GenreList.as_view()),
    path(r'platforms/', views.PlatformList.as_view()),

    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('registration', views.registration, name="registration"),
    path('', views.home, name="home"),
    url(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.activate, name='activate'),

]
