"""DjangoWebProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ColumbiaApp import views
from django.contrib.auth.views import LoginView,LogoutView,login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('doLogin',views.doLogin,name='doLogin'),
    path('register',views.register,name='register'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('restaurant_map',views.restaurant_map,name='restaurant_map'),
    path('fav_list',views.fav_list,name='fav_list'),
    path('add_to_fav',views.add_to_fav,name='add_to_fav'),
    path('remove_from_fav',views.remove_from_fav,name='remove_from_fav'),
    path('doRegister',views.doRegister,name='doRegister'),
    path('doAdminRegister',views.doAdminRegister,name='doAdminRegister'),
    path('user_profile',views.user_profile,name='user_profile'),
    path('user_profile_edit',views.user_profile_edit,name='user_profile_edit'),
    path('user_profile_update',views.user_profile_update,name='user_profile_update'),
]
