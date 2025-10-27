from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.lib.server.directory import get_user_dir
import subprocess
from pathlib import Path
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
