from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.lib.server.directory import get_user_dir
import subprocess
from pathlib import Path
from pygit2 import Repository, Commit, Tree, repository

# Create your views here. 
#
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
def fetch_repository(request, username, repository_name, oid="HEAD"):

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
            current_object = current_object.peel(Commit)
            entry_list = []

            for entry in current_object.tree:
                entry_list.append({
                    "name": entry.name,
                    "type": entry.type_str,
                    "oid": entry.id,
                })

            return Response({
                "status": True,
                "object":
                {
                    "type": current_object.type_str,
                    "oid": current_object.id,
                    "message": current_object.message,
                    "author": current_object.author.name,
                    "time":  current_object.commit_time,
                    "entries": entry_list,
                }
            })

        case "tree":
            print("tree")
        case "blob":
            print("blob")
        case "tag":
            print("tag")
        case _:
            print("not a valid git object")



