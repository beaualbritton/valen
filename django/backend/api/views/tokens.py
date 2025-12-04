from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, make_password
from api.models import Token 
import secrets, hashlib


@api_view(["POST"])
def create_token(request):
    try:
        user = request.user

        if not user.is_authenticated:
            return Response({"status": False, "message": "not logged in"})

        data = request.data
        
        creation = timezone.now()
        expiration = data.get("expiration")
        if not expiration:
            raise Exception("Set an expiration date")

        name = data.get("name")
        if not name:
            raise Exception("Name your token")

        # 32 bytes for 0-255 len token
        token = secrets.token_urlsafe(32)
        # using django's pw hash/salt
        hash = hashlib.sha256(token.encode()).hexdigest()

        token_entry = Token(user=user, name=name, hash=hash, creation=creation, expiration=expiration)
        token_entry.save()

        return Response({"status": True, "token": token})
    except Exception as e:
        return Response({"status": False, "token": None, "message": f"Error creating token: {e}"})


@api_view(["DELETE"])
def delete_token(request):
    try:
        user = request.user
        if not user.is_authenticated:
            raise Exception("Not logged in")

        data = request.data
        token = data.get("token")
        if not token:
            raise Exception("Provide a token name")

        token_entry = Token.objects.filter(user=user, name=token).first()

        if token_entry:
            token_entry.delete()

        return Response({"status": True, "message": f"Deleted token {token}"})

    except Exception as e:
        return Response({"status": False, "message": f"Failed to delete token: {e}"})


@api_view(["GET"])
def list_tokens(request):
    try:
        user = request.user
        if not user.is_authenticated:
            raise Exception("Not logged in")

        tokens = Token.objects.filter(user=user)
        token_names = []
        for token in tokens:
            token_names.append(token.name)

        if not token_names:
            raise Exception("No token to list")

        return Response({"status": True, "tokens": token_names})

    except Exception as e:
        return Response({"status": False, "tokens": None, "message": f"Failed to fetch: {e}"})
