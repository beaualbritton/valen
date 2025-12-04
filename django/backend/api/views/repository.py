from os import name
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
import subprocess
from pathlib import Path
from pygit2 import Repository, Commit, Tree 
from api.lib.git.peel import peel_commit, peel_blob, peel_tree
from api.lib.server.directory import get_user_dir
from api.models import Repository as Repository_Model
from api.serializers import RepositorySerializer

GIT_ROOT = Path("/srv/git")


@api_view(["POST"])
def create_repository(request):
    try:
        user = request.user
        if not user.is_authenticated:
            return Response({"status": False, "message": "not logged in"})

        repository_name = request.data.get("repository")
        description = request.data.get("description")
        is_public = request.data.get("visible")

        if get_user_dir(user.username):

            repo_path = Path(GIT_ROOT/user.username/f"{repository_name}.git")

            subprocess.run(["git", "init", "--bare", repo_path])
            subprocess.run(["touch", f"{repo_path}/git-daemon-export-ok"])
            subprocess.run(["git", "--git-dir", repo_path, "config", "http.receivepack", "true"])

            subprocess.run(["chmod", "-R", "g+rwX", repo_path])
            subprocess.run(["find", str(repo_path), "-type", "d", "-exec", "chmod", "2775", "{}", "+"])
            subprocess.run(["find", str(repo_path), "-type", "f", "-exec", "chmod", "664", "{}", "+"])

            # public by default, no collaborators
            new_repo = Repository_Model(owner=user, repo_name=f"{user}/{repository_name}", description=description, public=is_public)
            new_repo.save()

            return Response({"status": True, "message": f"repository {repository_name} created successfully."})
        else:
            raise Exception 

    except Exception as e:
        Response({"status": False, "message": f"repository  not created. {e}"})


@api_view(["POST"])
def delete_repository(request):
    try:
        user = request.user 
        if not user.is_authenticated:
            return Response({"status": False, "message": "not logged in"})

        repository_name = request.data.get("repository")
        if get_user_dir(user.username):
            repo_path = Path(GIT_ROOT/user.username/f"{repository_name}.git")
            subprocess.run(["rm", "-rf", repo_path])

            repo_entry = Repository_Model.objects.get(repo_name=f"{user.username}/{repository_name}")

            if repo_entry:
                repo_entry.delete()

            return Response({"status": True, "message": f"repository {repository_name} deleted successfully."})

        else:
            raise Exception("Repository doens't exist")

    except Exception as e:
        Response({"status": False, "message": f"repository  not created. {e}"})


@api_view(["GET"])
def fetch_repository(request, username, repository, oid="HEAD") -> Response:
    try:
        repo_path = Path(GIT_ROOT/username/f"{repository}.git/")
        git_repo = Repository(str(repo_path))

        current_object = None
        if oid == "HEAD":
            head = git_repo[git_repo.head.target]
            current_object = head
        else:
            current_object = git_repo.revparse_single(oid)

        object_type = current_object.type_str

        match object_type:
            case "commit":
                return peel_commit(current_object)
            case "tree":
                return peel_tree(current_object)
            case "blob":
                return peel_blob(current_object)
            case "tag":
                #TODO: implement
                raise Exception("Tags not implemented. How'd you get here?")

        raise Exception("Not a valid git object!")

    except Exception as e:
        Response({"status": False, "message": f"Error. {e}"})


@api_view(["GET"])
def fetch_repo_info(request, username, repository):
    try:
        repo_entry = Repository_Model.objects.get(repo_name=f"{username}/{repository}")
        user = request.user

        if not repo_entry.public:

            if not user.is_authenticated:
                raise Exception("not authenticated")

            if (user != repo_entry.owner) and user not in repo_entry.collaborators.all():
                raise Exception("not owner or collaborator")

        repo_serializer = RepositorySerializer(repo_entry)
        return Response({"status": True, "data": repo_serializer.data})

    except Exception as e:
        return Response({"status": False, "message": f"not authorized: {e}"})


@api_view(["GET"])
def fetch_repos_by_user(request, username):
    try:
        fetch_user = User.objects.get(username=username)

        if not fetch_user:
            raise Exception

        if (fetch_user == request.user) and request.user.is_authenticated:
            all_repositories = Repository_Model.objects.filter(owner=fetch_user)
        else:
            # using django's Q object for complex queries, effectively OR logic for orm
            # see: https://docs.djangoproject.com/en/5.2/topics/db/queries/#complex-lookups-with-q-objects
            all_repositories = Repository_Model.objects.filter(owner=fetch_user).filter(Q(public=True) | Q(collaborators=request.user)).distinct()

        serializer = RepositorySerializer(all_repositories, many=True)
        
        return Response({"status": True, "repositories": serializer.data})

    except Exception as e:
        return Response({"status": False, "message": f"error {e}", "repositories": None})


@api_view(["GET"])
def list_collaborators(request, username, repository):
    try:
        repo_entry = Repository_Model.objects.get(repo_name=f"{username}/{repository}")
        collaborators = []

        for c in repo_entry.collaborators.all():
            collaborators.append(c.username)

        if not collaborators:
            raise Exception("No collaborators to list.")

        return Response({"status": True, "collaborators": collaborators})

    except Exception as e:
        return Response({"status": False, "message": f"Error fetching collaborators: {e}", "collaborators": None})


@api_view(["POST"])
def add_collaborator(request):
    try:
        user = request.user
        if not user.is_authenticated:
            return Response({"status": False, "message": "not logged in"})

        repo_name = request.data.get("repository")
        repo_owner = request.data.get("owner")
        repo_entry = Repository_Model.objects.get(repo_name=f"{repo_owner}/{repo_name}")

        if user != repo_entry.owner:
            raise Exception("You must be the owner to add collaborators.")

        collaborator = request.data.get("collaborator")
        collaborator_entry = User.objects.get(username=collaborator)

        if not collaborator_entry:
            raise Exception(f"Couldn't find user {collaborator}")

        repo_entry.collaborators.add(collaborator_entry)

        return Response({"status": True, "collaborator": collaborator})

    except Exception as e:
        return Response({"status": False, "message": f"Error: adding collaborator: {e}", "collaborator": None})


@api_view(["POST"])
def remove_collaborator(request):
    try:
        user = request.user
        if not user.is_authenticated:
            raise Exception("Not logged in")

        repo_name = request.data.get("repository")
        repo_owner = request.data.get("owner")
        repo_entry = Repository_Model.objects.get(repo_name=f"{repo_owner}/{repo_name}")

        if user != repo_entry.owner:
            raise Exception("You must be the owner to remove collaborators")

        collaborator = request.data.get("collaborator")
        collaborator_entry = User.objects.get(username=collaborator)

        if not collaborator_entry:
            raise Exception(f"Couldn't find user {collaborator}")

        repo_entry.collaborators.remove(collaborator_entry)

        return Response({"status": True, "collaborator": collaborator})

    except Exception as e:
        return Response({"status": False, "message": f"error removing collaborator {e}"})


@api_view(["POST"])
def change_privacy(request):
    try:
        user = request.user
        if not user.is_authenticated:
            raise Exception("Not logged in")

        privacy_bool = request.data.get("public")

        repo_name = request.data.get("repository")
        repo_owner = request.data.get("owner")
        repo_entry = Repository_Model.objects.get(repo_name=f"{repo_owner}/{repo_name}")

        if user != repo_entry.owner:
            raise Exception("You must be the owner to change privacy")

        repo_entry.public = bool(privacy_bool)
        repo_entry.save()
        repo_serializer = RepositorySerializer(repo_entry)

        return Response({"status": True, "data": repo_serializer.data, "message": f"{repo_name} changed to {'public' if bool(privacy_bool) else 'private'}"})

    except Exception as e:
        return Response({"status": False, "data": None, "message": f"error chaging privacy {e}"})
        
