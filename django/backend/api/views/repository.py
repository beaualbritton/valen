from os import name
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
import subprocess
from pathlib import Path
from pygit2 import Repository, Commit, Tree, repository
from api.lib.git.peel import peel_commit, peel_blob, peel_tree
from api.lib.server.directory import get_user_dir
from api.models import Repository as Repository_Model

GIT_ROOT = Path("/srv/git")


@api_view(["POST"])
def create_repository(request):
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
        return Response({"status": False, "message": f"repository {repository_name} not created. Parent dir doesn't exist"})


@api_view(["POST"])
def delete_repository(request):
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
        return Response ({"status": False, "message": f"repository {repository_name} does not exist."})


@api_view(["GET"])
def fetch_repository(request, username, repository_name, oid="HEAD") -> Response :

    repo_path = Path(GIT_ROOT/username/f"{repository_name}.git/")
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
            print("tag")
    return Response({"status": False, "message": "not a valid git object"})


@api_view(["POST"])
def fetch_repos_by_user(request):
    try:
        username = request.data.get("username")
        fetch_user = User.objects.get(username=username)

        if not fetch_user:
            raise Exception

        all_repositories = Repository_Model.objects.filter(owner=fetch_user)
        repo_list = []

        if (fetch_user == request.user) and request.user.is_authenticated:
            for repo in all_repositories:
                repo_list.append(repo.repo_name)
        else:
            for repo in all_repositories:
                if repo.public:
                    repo_list.append(repo.repo_name)

        return Response({"status": True, "repositories": repo_list})

    except Exception:
        return Response({"status": False, "message": f"{username} doesn't exist", "repositories": None})


@api_view(["GET"])
def list_collaborators(request):
    try:
        repo_name = request.data.get("repository")
        repo_entry = Repository_Model.objects.get(repo_name=repo_name)
        collaborators = []

        for c in repo_entry.collaborators.all():
            collaborators.append(c.username)

        return Response({"status": True, "collaborators": collaborators, "count": len(collaborators)})

    except Exception:
        return Response ({"status": False, "collaborators": None, "message": "error fetching collaborators"})


@api_view(["POST"])
def add_collaborator(request):
    try:
        user = request.user
        if not user.is_authenticated:
            return Response({"status": False, "message": "not logged in"})

        repo_name = request.data.get("repository")
        repo_entry = Repository_Model.objects.get(repo_name=repo_name)

        if user != repo_entry.owner:
            raise Exception

        collaborator = request.data.get("collaborator")
        collaborator_entry = User.objects.get(username=collaborator)

        if not collaborator_entry:
            raise Exception

        repo_entry.collaborators.add(collaborator_entry)

        return Response({"status": True, "collaborator": collaborator})

    except Exception:
        return Response({"status": False, "message": "error adding collaborator"})


@api_view(["POST"])
def remove_collaborator(request):
    try:
        user = request.user
        if not user.is_authenticated:
            return Response({"status": False, "message": "not logged in"})

        repo_name = request.data.get("repository")
        repo_entry = Repository_Model.objects.get(repo_name=repo_name)

        if user != repo_entry.owner:
            raise Exception

        collaborator = request.data.get("collaborator")
        collaborator_entry = User.objects.get(username=collaborator)

        if not collaborator_entry:
            raise Exception

        repo_entry.collaborators.remove(collaborator_entry)

        return Response({"status": True, "removed": collaborator})

    except Exception:
        return Response({"status": False, "message": "error removing collaborator"})
