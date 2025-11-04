"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from api.views import create_repository, register_user, login_user, csrf_token, logout_user
from api.views import fetch_repository, fetch_repos_by_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', register_user),
    path('api/login/', login_user),
    path('api/csrf/', csrf_token),
    path('api/logout/', logout_user),
    path('api/public/repo/create/', create_repository),
    path('api/public/repo/by/<str:username>/<str:repository_name>/', fetch_repository),
    path('api/public/repo/by/<str:username>/<str:repository_name>/<str:oid>/', fetch_repository),
    path('api/public/repo/all/<str:username>/', fetch_repos_by_user)
]
