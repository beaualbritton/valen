from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
import subprocess
from pathlib import Path
from pygit2 import Repository
from api.lib.git.branch import get_branches, get_default_branch

GIT_ROOT = Path("/srv/git")


@api_view(["GET"])
def fetch_all_branches(request, username, repository):
    try:
        repo_path = Path(GIT_ROOT/username/f"{repository}.git")
        git_repo = Repository(str(repo_path))
        return get_branches(git_repo)

    except Exception as e:
        return Response({"status": False, "message": e})


@api_view(["GET"])
def fetch_default_branch(request, username, repository):
    try:
        repo_path = Path(GIT_ROOT/username/f"{repository}.git")
        git_repo = Repository(str(repo_path))
        return get_default_branch(git_repo)

    except Exception as e:
        return Response({"status": False, "message": e})

