from django.conf.urls import url

from . import views

urlpatterns = [
    url('^must$', views.must, name="must"),
    url('^game/(?P<game_id>[0-9]+)/$', views.game_description, name="game"),
    url('^$', views.home, name="home"),
    url('^login$', views.login, name="login"),
    url('^logout$', views.logout, name="logout"),
    url('^registration$', views.registration, name="registration"),
    url('^filter/$', views.filtered_games, name="filter"),
    url('^create-must/(?P<game_id>[0-9]+)/$', views.create_must, name="create-must"),
    url('^remove-must/(?P<game_id>[0-9]+)/$', views.remove_must, name="remove-must"),
    url('^get-particle-games/(?P<offset>[0-9]+)/$', views.get_particle_games, name="get-particle-games"),
    url('^search/(?P<search_string>[^/]+)$', views.search, name="search")
]

