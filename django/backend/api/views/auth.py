from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.middleware.csrf import get_token
from api.models import Profile
from api.lib.server.directory import create_user_dir
# aliases
create_user = User.objects.create_user

@api_view(["POST"])
def register_user(request):
    r_data = request.data
    username = r_data.get("username")
    password = r_data.get("password")

    if not username:
        return Response({"status": False, "message": "enter a username please!"})
    if not password:
        return Response({"status": False, "message": "enter a password please!"})

    user_exists: bool = User.objects.filter(username=username).exists()

    if user_exists:
        return Response({"status": False, "message": "username taken!"})

    # At this point, no errors
    new_user = create_user(username=username, password=password)

    # Create folder for user in /srv/git 
    user_dir = create_user_dir(username)

    # Create a new Profile associated with new_user
    new_profile = Profile.objects.create(user=new_user)

    if new_profile and user_dir:
        return Response({"status": True, "message": f"registration succesful for {username}"})
    else:
        return Response({"status": False, "message": f"registration unsuccesful for {username}"})


@api_view(["POST"])
def login_user(request):
    r_data = request.data
    username = r_data.get("username")
    password = r_data.get("password")

    if not username:
        return Response({"status": False, "message": "enter a username please!"})
    if not password:
        return Response({"status": False, "message": "enter a username please!"})

    user_authenticated = authenticate(request, username=username, password=password)

    if user_authenticated:
        login(request, user_authenticated)
        return Response({"status": True, "message": f"login succesful for {username}"})
    else:
        return Response({"status": False, "message": f"invalid login for {username}"})


@api_view(["POST"])
def logout_user(request):
    logout(request)
    return Response({"status": True, "message": "logged out!"})


@api_view(["GET"])
def csrf_token(request):
    return JsonResponse({"csrfToken": get_token(request)})
