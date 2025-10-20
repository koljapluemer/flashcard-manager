from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, home, settings

urlpatterns = [
    path('', home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('settings/', settings, name='settings'),
]