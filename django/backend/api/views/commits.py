from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.lib.server.directory import get_user_dir
import subprocess
from pathlib import Path
from pygit2 import Repository, Commit, Tree
from api.lib.git.commits import all_commits, find_commit_refs, find_latest_ref

GIT_ROOT = Path("/srv/git")


#TODO: validate user/repo lib function returning t/f if both user and repo exist
@api_view(["GET"])
def fetch_commits_for_repo(request,username,repository):
    repo_path = Path(GIT_ROOT/username/f"{repository}.git")
    git_repo = Repository(str(repo_path))
    return all_commits(git_repo)


@api_view(["GET"])
def fetch_commits_for_object(request,username,repository,oid):
    repo_path = Path(GIT_ROOT/username/f"{repository}.git")
    git_repo = Repository(str(repo_path))
    git_object = git_repo.revparse_single(oid)
    return find_commit_refs(git_repo, git_object)


@api_view(["GET"])
def fetch_latest_commit_for_object(request, username, repository, oid, relative_commit_oid):
    repo_path = Path(GIT_ROOT/username/f"{repository}.git")
    git_repo = Repository(str(repo_path))
    git_object = git_repo.revparse_single(oid)
    return find_latest_ref(git_repo, git_object, relative_commit_oid)
