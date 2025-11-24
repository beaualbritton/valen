from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, make_password
from api.models import Token 
import secrets, hashlib

@api_view(["POST"])
def create_token(request):
    user = request.user

    if not user.is_authenticated:
        return Response({"status": False, "message": "not logged in"})

    data = request.data
    
    creation = timezone.now()
    expiration = data.get("expiration")
    if not expiration:
        return Response({"status": False, "message": "set an expiration date"})

    name = data.get("name")
    if not name:
        return Response({"status": False, "message": "name your token"})

    # 32 bytes for 0-255 len token
    token = secrets.token_urlsafe(32)
    # using django's pw hash/salt
    hash = hashlib.sha256(token.encode()).hexdigest()

    token_entry = Token(user=user, name=name, hash=hash, creation=creation, expiration=expiration)
    token_entry.save()

    return Response({"status": True, "token": token})


@api_view(["DELETE"])
def delete_token(request):
    user = request.user
    if not user.is_authenticated:
        return Response({"status": False, "message": "not logged in"})

    data = request.data
    token = data.get("token")
    if not token:
        return Response({"status": False, "message": "token not provided"})

    hash = make_password(token)
    token_entry = Token.objects.get(hash=hash)

    if token_entry:
        token_entry.delete()

    return Response({"status": True, "message": "deleted token"})


@api_view(["GET"])
def list_tokens(request):
    user = request.user
    if not user.is_authenticated:
        return Response({"status": False, "message": "not logged in"})

    tokens = Token.objects.filter(user=user)
    token_names = []
    for token in tokens:
        token_names.append(token.name)

    if not token_names:
        return Response({"status": False, "message": "no tokens to list"})

    return Response({"status": True, "tokens": token_names})
