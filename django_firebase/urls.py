"""django_firebase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.signin,name='signin'),
    path('signin/',views.authenticate,name='authenticate'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('create_report/',views.create_report,name='create_report'),
    path('retriew_report/',views.retriew_report,name='retriew_report')
]
