from django.conf.urls import url

from . import views

urlpatterns = [
    url('^must$', views.must),
    url('^game/(?P<game_id>[0-9]+)/$', views.game_description),
    url('^$', views.home),
    url('^login$', views.login),
    url('^logout$', views.logout),
    url('^registration$', views.registration),
    url('^filter/$', views.filtered_games),
    url('^create-must/(?P<game_id>[0-9]+)/$', views.create_must),
    url('^remove-must/(?P<game_id>[0-9]+)/$', views.remove_must),
    url('^get-particle-games/(?P<offset>[0-9]+)/$', views.get_particle_games),
]

