import base64, hashlib
from api.views import repository
from rest_framework.decorators import api_view
from django.core.cache import cache
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
from api.lib.git.resolve import resolve_repo_http, resolve_repo_ssh
from api.models import Token, Repository
from pathlib import Path

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

    auth = request.META.get("HTTP_AUTHORIZATION", "")

    repo_name = resolve_repo_http(uri)

    repo_key = f"repo_key:{repo_name}"
    repo = cache.get(repo_key)
    if repo is None:
        repo = Repository.objects.get(repo_name=repo_name)
        cache.set(repo_key, repo, 30)


    user = None
    is_valid = False
    if auth.startswith("Basic "):
        try:
            b64_decode = base64.b64decode(auth[6:]).decode()
            b64_decode = b64_decode.split(":", 1)
            username = b64_decode[0]
            auth_token = b64_decode[1]

            auth_token_hash = hashlib.sha256(auth_token.encode()).hexdigest()

            auth_cache_key = f"auth:{user}:{auth_token_hash[:16]}"
            cached_result = cache.get(auth_cache_key)

            if cached_result:
                user, is_valid = cached_result
                
            else:
                user = User.objects.get(username=username)
                is_valid = Token.objects.filter(user=user, hash=auth_token_hash).exists()
                cache.set(auth_cache_key, (user, is_valid), 30)

            if not is_valid:
                return authenticate_res
        except Exception:
            return authenticate_res

    
    if "git-upload-pack" in uri:
        if repo.public:
            print("public")
            return HttpResponse(status=200)

        #TODO: collaborators
        elif user and (user == repo.owner):
            print("private but owner")

            if is_valid:
                return HttpResponse(status=200)

        else:
            print("private")

    if "git-receive-pack" in uri:
        #TODO: collaborators
        if user and (user == repo.owner):
            print("owner push")

            if is_valid:
                return HttpResponse(status=200)

    return authenticate_res


@api_view(["GET"])
def get_user(request):
    user = request.user
    if not user or not user.is_authenticated:
        return Response({"status": False, "message": "not logged in"})

    return Response({"status": True, "user": UserSerializer(user).data})

@csrf_exempt
@api_view(['POST'])
def ssh_validation(request):
    # sent from validate_ssh script 
    user = request.data.get("username")
    command = request.data.get("command")

    repo_name = resolve_repo_ssh(command)

    repo = Repository.objects.get(repo_name=repo_name)
    
    user = User.objects.get(username=user)
    print(user.username)
    print(command)
    print(repo.repo_name)

    if "git-upload-pack" in command:
        print("clone")
        if repo.public:
            print("public")
            return Response({"allowed": True})
        #TODO: collaborators
        elif (user == repo.owner):
            print("private but owner ")
            return Response({"allowed": True})
        else:
            print("private")

    elif "git-receive-pack" in command:
        print("push")
        # TODO: collaborators
        if (user == repo.owner):
            print("owner push")
            return Response({"allowed": True})
        else:
            print("anon push")

    return Response({"allowed": False})


@api_view(["POST"])
def add_ssh_key(request):
    # authorized keys are stored here, identify each key with a user 
    AUTHORIZED_KEYS = Path("/srv/git/.ssh/authorized_keys")

    try:
        # sent from git server for ssh validation
        pub_key = request.POST.get('public_key')
        pub_key = pub_key.strip()

        if pub_key.startswith("ssh"):
            # write to authorized_keys
            line = f'environment="SSH_USER={request.user.username}",command="/usr/local/bin/validate_ssh" {pub_key}'

            with open(AUTHORIZED_KEYS, 'a') as key_file:
                key_file.write(f"{line}\n")
        else:
            raise Exception("not a valid key")

        return Response({"status": True})

    except Exception:
        return Response({"status": False})
