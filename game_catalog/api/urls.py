from django.conf.urls import url
from . import views

urlpatterns = [
    url('^must$', views.must),
    url('^game/(?P<game_id>[0-9]+)/$', views.game_description),
    url('^$', views.home),
    url('^ajax/filter/$', views.filtered_games),
    url('^login$', views.login),
    url('^logout$', views.logout),
]
