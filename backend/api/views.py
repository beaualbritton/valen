from rest_framework.decorators import api_view
from rest_framework.response import Response
import subprocess
# Create your views here. 


@api_view(["POST"])
def create_repository(request):
    print(f"header: {request.headers}")
    print(request.content_type)
    print(f"body: {request.body}")
    print(f"data: {request.data}")
    repository_name = request.data.get("repository")
    print(repository_name)
    repo_path = f"/srv/git/{repository_name}.git"

    subprocess.run(["git", "init", "--bare", repo_path])
    subprocess.run(["touch", f"{repo_path}/git-daemon-export-ok"])
    subprocess.run(["git", "--git-dir", repo_path, "config", "http.receivepack", "true"])
    subprocess.run(["chown", "-R", "www-data:www-data", repo_path])

    return Response({"status": True, "message": f"repository {repository_name} created successfully."})
