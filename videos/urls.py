
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('details/<str:videoId>', views.videos_details, name='details'),
    path('create_playlist', views.create_playlist, name='create_pl'),


]
