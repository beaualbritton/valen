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
from api.views import check, create_repository, register_user, login_user, csrf_token, logout_user, get_user
from api.views import fetch_repository, fetch_repos_by_user
from api.views import fetch_commits_for_repo, fetch_commits_for_object, fetch_latest_commit_for_object
from api.views import fetch_all_branches, fetch_default_branch
from api.views import create_token, delete_token, list_tokens, git_authentication
from api.views import ssh_validation, add_ssh_key

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/check', check),
    path('api/register/', register_user),
    path('api/login/', login_user),
    path('api/csrf/', csrf_token),
    path('api/logout/', logout_user),
    path('api/user/', get_user),
    path('api/auth/git/', git_authentication),
    path('api/auth/ssh/', ssh_validation),
    path('api/public/ssh/add', add_ssh_key),
    path('api/public/token/create/', create_token),
    path('api/public/token/delete/', delete_token),
    path('api/public/token/list/', list_tokens),

    path('api/public/repo/create/', create_repository),
    path('api/public/repo/by/<str:username>/<str:repository_name>/', fetch_repository),
    path('api/public/repo/by/<str:username>/<str:repository_name>/<str:oid>/', fetch_repository),
    path('api/public/repo/all/<str:username>/', fetch_repos_by_user),

    path('api/public/repo/commits/<str:username>/<str:repository>/', fetch_commits_for_repo),
    path('api/public/repo/commits/<str:username>/<str:repository>/<str:oid>/', fetch_commits_for_object),
    path('api/public/repo/commits/<str:username>/<str:repository>/<str:oid>/latest', fetch_latest_commit_for_object),

    path('api/public/repo/branches/<str:username>/<str:repository>/', fetch_all_branches),
    path('api/public/repo/branches/<str:username>/<str:repository>/default', fetch_default_branch)
]
