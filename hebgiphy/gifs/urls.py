from django.urls import path

from . import views


urlpatterns = [
    path('search/', views.gif_search, name='search'),
    path('favorite/<str:giphy_id>', views.gif_favorite, name='favorite'),
    path('tags/<str:giphy_id>', views.gif_tags, name='tags'),
    path('favorites/', views.gif_favorite_list, name='favorites'),
]
