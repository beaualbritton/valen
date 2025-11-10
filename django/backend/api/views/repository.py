from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
import subprocess
from pathlib import Path
from pygit2 import Repository, Commit, Tree, repository
from api.lib.git.peel import peel_commit, peel_blob, peel_tree
from api.lib.server.directory import get_user_dir

GIT_ROOT = Path("/srv/git")


@api_view(["POST"])
def create_repository(request):
    user = request.user
    if not user.is_authenticated:
        return Response({"status": False, "message": "not logged in"})

    repository_name = request.data.get("repository")
    if get_user_dir(user.username):

        repo_path = Path(GIT_ROOT/user.username/f"{repository_name}.git")

        subprocess.run(["git", "init", "--bare", repo_path])
        subprocess.run(["touch", f"{repo_path}/git-daemon-export-ok"])
        subprocess.run(["git", "--git-dir", repo_path, "config", "http.receivepack", "true"])
        subprocess.run(["chown", "-R", "www-data:www-data", repo_path])

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
        subprocess.run(["rm","-rf", repo_path])
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


@api_view(["GET"])
def fetch_repos_by_user(request, username):
    user_exists: bool = User.objects.filter(username=username).exists()
    if not user_exists:
        return Response({"status": False, "message": f"{username} doesn't exist", "repositories": None})

    user_dir = Path(GIT_ROOT/username)
    repos = []
    for child in user_dir.iterdir():
        if child.is_dir():
            repos.append(child.stem)

    return Response({"status": True, "repositories": repos})
