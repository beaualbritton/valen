import base64
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.middleware.csrf import get_token
from api.serializers import UserSerializer
from api.models import Profile
from api.lib.server.directory import create_user_dir
from api.models import Token
# aliases
create_user = User.objects.create_user


@api_view(["GET"])
def check(request):
    return Response(status=200)


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


@csrf_exempt
def git_authentication(request):
    # git sends tokens thru http -> Authorization: Basic <base64hash>
    uri = request.META.get("HTTP_X_ORIGINAL_URI", "")

    # return 401 with authenticate header by default
    authenticate_res = HttpResponse(status=401)
    authenticate_res["WWW-Authenticate"] = 'Basic realm="Git"'

    if "git-upload-pack" in uri:
        return HttpResponse(status=200)

    if "git-receive-pack" in uri:
        try:
            auth = request.META.get("HTTP_AUTHORIZATION", "")

            if not auth.startswith("Basic "):
                return authenticate_res

            b64_decode = base64.b64decode(auth[6:]).decode()
            b64_decode = b64_decode.split(":", 1)

            username = b64_decode[0]
            auth_token = b64_decode[1]

            user = User.objects.get(username=username)
            user_tokens = Token.objects.filter(user=user)

            for token in user_tokens:
                if check_password(auth_token, token.hash):
                    return HttpResponse(status=200)

        except Exception:
            return authenticate_res

    return authenticate_res


@api_view(["GET"])
def get_user(request):
    user = request.user
    if not user or not user.is_authenticated:
        return Response({"status": False, "message": "not logged in"})

    return Response({"status": True, "user": UserSerializer(user).data})
