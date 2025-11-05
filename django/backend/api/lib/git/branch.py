from pygit2 import Repository
from rest_framework.response import Response


# all branches for a repo
def get_branches(git_repo) -> Response:
    branch_list = list(git_repo.branches)
    return Response({"status":True, "branches": branch_list})


# get default branch from a repo: the branch that HEAD points to
def get_default_branch(git_repo: Repository) -> Response:
    default = git_repo.head.shorthand
    return Response({"status": True, "branches": default})
