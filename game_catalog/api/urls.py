from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [

    path('must/', views.must, name="must"),
    path('game/<int:game_id>/', views.game_description, name="game"),
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('registration/', views.registration, name="registration"),
    path('filter/', views.filtered_games, name="filter"),
    path('create-must/<int:game_id>', views.create_must, name="create-must"),
    path('remove-must/<int:game_id>', views.remove_must, name="remove-must"),
    path('get-particle-games/<int:offset>', views.get_particle_games, name="get-particle-games"),
    path('search/<str:search_string>', views.search, name="search"),
    url(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.activate, name='activate'),
    url('/*', TemplateView.as_view(template_name='page_404.html'))

]
