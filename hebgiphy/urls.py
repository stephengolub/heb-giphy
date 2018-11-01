from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from hebgiphy.ui.views import home_view


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('gifs/', include('hebgiphy.gifs.urls')),
    path('admin/', admin.site.urls),
    path('', home_view, name="index"),
]
