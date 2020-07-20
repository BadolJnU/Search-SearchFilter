from django.contrib import admin
from django.urls import path, include
from home import views
from home.views import *

app_name = "home"

urlpatterns = [
    path('',views.home, name='home'),
    path('about/',views.about, name='about'),
    path('search/',views.search,name='search'),
    path('signup',views.handleSignup,name='handleSignup'),
    path('login',views.handleLogin,name='handleLogin'),
    path('logout',views.handleLogout,name='handleLogout'),
    path('searchHistory/',views.searchHistory,name='searchHistory'),
    path("HomeListing/", HomeListing.as_view(), name = 'listing'),
    path("ajax/loginuser/", getLoginuser, name = 'get_loginuser'),
    path("ajax/keyword/", getKeyword, name = 'get_keyword'),
]