from django.urls import path

from . import views


urlpatterns = [
    path('search/', views.gif_search, name='gif_search'),
]
